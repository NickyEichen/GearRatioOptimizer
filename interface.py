from ipywidgets import interact_manual, FloatText
import ipywidgets as widgets
from graphGeneratorWithDefault import graphRatio

style = {'description_width': 'initial'}
layout_hidden=widgets.Layout(visibility="visible") # visible or hidden
disabled_true = True

        
distance_w = widgets.FloatText(value=0.8, description='Distance (m): ', style=style)
mass_w = widgets.FloatText(value=30, description='Robot Mass (lbs): ', style=style)

motor_num_w = FloatText(value=4, description='Number of Motors: ', style=style)

# motor type
motor_type_w = widgets.Dropdown(options=[("AndyMark NeveRest", "nr"), 
                                         ("CIM", "cim"),
                                         ("775pro", "775"), 
                                         ("other (input all parameters)", "other_m")], 
                                description="Motor Type: ",
                                value="nr", style=style)
def update_widget_m(w, d):
    w.value = d[motor_type_w.value]
    if motor_type_w.value == "other_m":
        #w.layout.visibility = "visible"
        w.disabled = False
    else:
        #w.layout.visibility = "hidden"
        w.disabled = True

# motor data from https://motors.vex.com
free_speed_default =      {"nr" : 5476,    "cim" : 5330,   "775" : 18730, "other_m": 1}
no_load_current_default = {"nr" : 0.355,   "cim" : 2.7,    "775" : 0.7,   "other_m": 1}
stall_torque_default =    {"nr" : 0.173,   "cim" : 2.41,   "775" : 0.71,  "other_m": 1}
stall_current_default =   {"nr" : 9.801,   "cim" : 131,    "775" : 134,   "other_m": 1}

# values whose default are set by motor type
#free speed
free_speed_w = FloatText(value=free_speed_default["nr"], description = '---- Free Speed (rpm): ', 
                         style=style, layout=layout_hidden, disabled=disabled_true)
def update_free_speed(*args):
    update_widget_m(free_speed_w, free_speed_default)
motor_type_w.observe(update_free_speed, 'value')

# no load current
no_load_current_w = FloatText(value=no_load_current_default["nr"], description='---- Free Current (Amps): ', 
                              style=style, layout=layout_hidden, disabled=disabled_true)
def update_no_load_current(*args):
    update_widget_m(no_load_current_w, no_load_current_default)
motor_type_w.observe(update_no_load_current, 'value')

# stall torque
stall_torque_w = FloatText(value=stall_torque_default["nr"], description='---- Stall Torque (Nm): ', 
                           style=style, layout=layout_hidden, disabled=disabled_true)
def update_stall_torque(*args):
    update_widget_m(stall_torque_w, stall_torque_default)
motor_type_w.observe(update_stall_torque, 'value')

# stall current
stall_current_w = FloatText(value=stall_current_default["nr"], description='---- Stall Current (Amps): ', 
                            style=style, layout=layout_hidden, disabled=disabled_true)
def update_stall_current(*args):
    update_widget_m(stall_current_w, stall_current_default)
motor_type_w.observe(update_stall_current, 'value')

minRatio_w = FloatText(value=5, description='Minimum Ratio: ', style=style)
maxRatio_w = FloatText(value=40, description='Maximum Ratio: ', style=style)
nominal_voltage_w = FloatText(value=12, description='Motor Nominal Voltage (V): ', style=style)
battery_resistance_w = FloatText(value=0.1, description = 'Battery Internal Resistance (Ohms): ', style=style)
operating_voltage_w = FloatText(value=12.7, description='Operating Voltage (v): ', style=style)

# wheel type
wheel_type_w = widgets.Dropdown(options=[("AndyMark Standard Mecanum 4in", "am_sm4"),
                                         ("AndyMark HD Mecanum Wheels 4in", "am_hdm4"),
                                         ("AndyMark Duraomni Omniwheel 4in", "am_do4"),
                                         ("AndyMark Stealth Wheel 4in", "am_sw4"),
                                         ("Nexus Mecanum Wheel 4in", "n_m4"),
                                         ("VexPro Mecanum 4in", "vp_m4"),
                                         ("VexPro Colson 4/0.85in", "vp_c48"),
                                         ("VexPro Colson 4/1.5in", "vp_c415"),
                                         ("VexPro Colson 4/1.5in", "vp_c415"),
                                         ("VexPro Colson 3.5/1.5in", "vp_c3515"),
                                         ("VexPro Colson 3/0.8in", "vp_c38"),
                                         ("VexPro Colson 3/1.5in", "vp_c315"),
                                         ("VexPro Omni 3.25in", "vp_o325"),
                                         ("VexPro Omni 4in", "vp_o4"),
                                         ("BaneBot T80 3.75in", "bb_t8375"),
                                         ("Others (input all parameters)", "other_w")],
                                description="Wheel Type: ",
                                value="am_sm4", style=style)
def update_widget_w(w, d):
    w.value = d[wheel_type_w.value]
    if wheel_type_w.value == "other_w":
        #w.layout.visibility = "visible"
        w.disabled = False
    else:
        #w.layout.visibility = "hidden"
        w.disabled = True


def compute_inertia(mass, radius): # mm * gr
    return (mass/100) * (radius/1000) * (radius/1000) / 2

radius_default = {"am_sm4" :  50.8,
                  "am_hdm4":  50.8,
                  "am_do4":   50.8,
                  "am_sw4":   50.8,
                  "n_m4":     50,
                  "vp_m4":    50.8,
                  "vp_c48":   50.8,
                  "vp_c415":  50.8,
                  "vp_c3515": 88.9/2,
                  "vp_c38":   76.2/2,
                  "vp_c315":  76.2/2,
                  "vp_o325":  82.6/2,
                  "vp_o4":    50.8,
                  "bb_t8375": 95.2/2,
                  "other_w":  50.8}
wheel_efficiency_default = {"am_sm4" :  0.7,
                            "am_hdm4":  0.7,
                            "am_do4":   1,
                            "am_sw4":   1,
                            "n_m4":     0.7,
                            "vp_m4":    0.7,
                            "vp_c48":   1,
                            "vp_c415":  1,
                            "vp_c3515": 1,
                            "vp_c38":   1,
                            "vp_c315":  1,
                            "vp_o325":  1,
                            "vp_o4":    1,
                            "bb_t8375": 1,
                            "other_w":  1}
intertia_default = {"am_sm4" : compute_inertia(50.8,   158),
                    "am_hdm4": compute_inertia(50.8,   400),
                    "am_do4":  compute_inertia(50.8,   268),
                    "am_sw4":  compute_inertia(50.8,   108),
                    "n_m4":    compute_inertia(50.8,   400),
                    "vp_m4":    compute_inertia(50.8,   249),
                    "vp_c48":   compute_inertia(50.8,   118),
                    "vp_c415":  compute_inertia(50.8,   240),
                    "vp_c3515": compute_inertia(88.9/2, 145),
                    "vp_c38":   compute_inertia(76.2/2, 72),
                    "vp_c315":  compute_inertia(76.2/2, 150),
                    "vp_o325":  compute_inertia(82.6/2, 177),
                    "vp_o4":    compute_inertia(50.8,   236),
                    "bb_t8375": compute_inertia(95.2/2, 113),
                    "other_w":  compute_inertia(50.8,   100)}

radius_w = FloatText(value=radius_default["am_sm4"], description='---- Radius (mm): ',
                     style=style, layout=layout_hidden, disabled=disabled_true)
def update_radius(*args):
    update_widget_w(radius_w, radius_default);
wheel_type_w.observe(update_radius, 'value')


wheel_efficiency_w = FloatText(value=wheel_efficiency_default["am_sm4"], description='---- Efficiency: ',
                               style=style, layout=layout_hidden, disabled=disabled_true)
def update_wheel_efficiency(*args):
    update_widget_w(wheel_efficiency_w, wheel_efficiency_default)
wheel_type_w.observe(update_wheel_efficiency, 'value')

intertia_w = FloatText(value=intertia_default["am_sm4"], description='---- Rotational Inertia (kg m^2): ',
                       style=style, layout=layout_hidden, disabled=disabled_true)
def update_intertia(*args):
    update_widget_w(intertia_w, intertia_default);
wheel_type_w.observe(update_intertia, 'value')


interact_manual(graphRatio, 
                distance = distance_w,
                mass = mass_w,
                motor_num = motor_num_w,
                motor_type = motor_type_w,
                stall_torque = stall_torque_w,
                stall_current = stall_current_w,
                free_speed = free_speed_w,

                wheel_type = wheel_type_w,
                radius = radius_w,
                inertia = intertia_w,                
                wheel_efficiency = wheel_efficiency_w,

                minRatio = minRatio_w,
                maxRatio = maxRatio_w,
                no_load_current = no_load_current_w,
                nominal_voltage = nominal_voltage_w,
                batery_resistance = battery_resistance_w,
                operating_voltage = operating_voltage_w,
               )

print()
