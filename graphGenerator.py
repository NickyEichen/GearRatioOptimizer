import numpy as np
import math
import matplotlib.pyplot as plt
import sympy

from IPython.display import display, clear_output

from sympy import *



#Symbols
km, ke = symbols('k_m k_e', constant=True, real=True, ) # Proportionality Constants (torque & emf)
Vo, Ve, Tm, Tf = symbols('V_o V_e T_m T_f', constant=True, real=True) # Supplied Voltage, Emf voltage, Motor Torque, Frictional Torque
I, rm, rb = symbols('I r_m r_b', constant=True, real=True) # Current, motor resistance, battery resistance
w = symbols('w', constant=True, real=True) # (omega) motor rotational speed

#More symbols
Tnet, rw, E= symbols('T_net r_w, E', constant=True, real=True) # net torque, wheel radius, Wheel efficiency
Iw, m = symbols('I_w m', constant=True, real=True) # Wheel inertia, robot mass
g = symbols('g', constant=True, real=True) # Gear ratio

# More Symbols
v = symbols('v', constant=True, real=True) # Robot velocity

# Motor Constant Symbols
Ts, Is, Io, wo, nm, Vm = symbols('T_s I_s I_o w_o nm V_m', constant=True, real=True) # Stall Torque, Stall Current, Free current, number of motors, nominal voltage



# Acceleration Definition
acelDef = Tnet / (rw*m/E + Iw/rw)

# Torque Definition
TorqueDef = km * (Vo - w*ke)/(rm + rb) - Tf

# Rotational Velocity Definition
wDef = v/(math.pi*rw )* 60 * g
vDef = solve(Eq(wDef, w), v)

# Motor Constant Definitions
KmDef = Ts / Is
KeDef = Vm / wo
RmDef = Vm / (Is * nm)
TfDef = Ts * Io * nm / Is

# Manipulations
workingAcel = simplify(acelDef.subs(Tnet, TorqueDef * g))
workingAcel2 = workingAcel.subs(w, wDef)
workingAcel3 = workingAcel2.subs([(km, KmDef), (ke, KeDef), (rm, RmDef), (Tf, TfDef)])


def graphRatio(distance, minRatio, maxRatio, stall_torque, motor_num, stall_current, no_load_current,
                nominal_voltage, free_speed, radius, batery_resistance, wheel_efficiency, operating_voltage,
                inertia, mass):
        
    def aceleration(vel, gratio):
        return FVAL*gratio + SVAL *gratio*gratio*vel

    def timeAtRatio(targetDist, ratio):
        assert(not ratio == 0)
        t_acum = 0
        x_acum = 0
        v_acum = 0
        dt= 0.0005
        while x_acum < targetDist:
            a = aceleration(v_acum, ratio)
            v_acum += a*dt
            x_acum += v_acum*dt
            t_acum += dt
            if a < 0:
                print("Error, the gear ratio is too low")
                return(0)
            if t_acum > 10:
                print('Error, the time is greater than 10 seconds')
                return(0)
        return t_acum

    
    subList = [(Ts, stall_torque), (nm, motor_num), (Is, stall_current), (Io, no_load_current), 
                     (Vm, nominal_voltage), (wo, free_speed), (rw, radius), (rb, batery_resistance), 
                     (E, wheel_efficiency), (Vo, operating_voltage), (Iw, inertia), (m, mass)]

    acelExp = workingAcel3.subs(subList)

    if wheel_efficiency == 1:
        wheelType = 'Tank Drive'
    elif wheel_efficiency == 0.7:
        wheelType = 'Mecanum Drive'
    else:
        wheelType = '' + 100 * wheel_efficiency + '% efficiency'

    FCOMP, SCOMP = acelExp.expand().args
    FVAL = float(FCOMP.subs(g, 1))
    SVAL = float(SCOMP.subs([(g, 1), (v, 1)]))
    
    progressBar = widgets.FloatProgress(min=minRatio, max=maxRatio, description='Calculating:')
    display(progressBar)
    def updateStatus(ratio):
        progressBar.value = ratio
        return None
        
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ratios = np.arange(minRatio, maxRatio, .1)

    time = [updateStatus(x) or timeAtRatio(distance, x) for x in ratios]

    minTime = min(time)
    index = time.index(minTime)
    minRatio = ratios[index]

    label = 'Min: %.1f:1 (%.3fs)' %(minRatio, minTime)
    ax.plot(ratios, time, label=label, color='blue')
    ax.plot(minRatio, minTime, '-o', color='blue')

    ax.set_xlabel("Gear Reduction", fontsize=15)
    ax.set_ylabel("Time", fontsize=18)
    ax.legend(loc="best")
    ax.set_title('%s  |  Mass = %.1f lbs | Dist = %.1f m' %(wheelType, mass*2.20462, distance), fontsize=13)
    ax.margins(0.1)
    fig.tight_layout()
    
    clear_output()
    
    plt.show()