from dearpygui.core import *
from dearpygui.simple import *
from math import cos, sin


# callbacks

gl = 0

#def plot_callback(sender, data):
def plot_callback():
    global gl
    clear_plot("Plot")

    data1x = []
    data1y = []
    for i in range(0, 100):
        data1x.append(3.14 * i / 180)
        data1y.append(cos(3 * 3.14 * i / 180 + gl))

    data2x = []
    data2y = []
    for i in range(0, 100):
        data2x.append(3.14 * i / 180)
        data2y.append(sin(2 * 3.14 * i / 180 + gl))

    add_line_series("Plot", "Cos", data1x, data1y, weight=2)
    add_line_series("Plot", "Sin", data2x, data2y, weight=2)
    # add_shade_series("Plot", "Cos Area", data1x, data1y, y2=[0.0]*100, weight=2, fill=[255, 0, 0, 100])
    # add_scatter_series("Plot", "Sin", data2x, data2y)


def test():
    pass


with window("Main Window"):
    with group("Left Panel", width=250):
        # add_button("Plot data", callback=plot_callback)
        add_text("Connection params")
        add_input_text("Address", source="address", width=200)
        add_input_text("Port", source="address", width=200)
        add_button("Connect", callback=test)
        ## Params
        add_text("Model params")
        add_input_text("jam_pos_in", source="1", width=200)
        add_input_text("F_set", source="2", width=200)
        add_input_text("shaker_amp", source="3", width=200)
        add_input_text("kShaker", source="4", width=200)
        add_input_text("m", source="5", width=200)
        add_input_text("f_mode2", source="6", width=200)
        add_input_text("f_mode3", source="7", width=200)
        add_input_text("F_setd", source="8", width=200)
        add_input_text("a_mode5", source="9", width=200)
        add_input_text("b_mode5", source="10", width=200)
        add_input_text("c_mode5", source="11", width=200)
        add_input_text("d_mode5", source="12", width=200)
        add_input_text("g_mode5", source="13", width=200)
        add_input_text("v_mode6", source="14", width=200)
        add_input_text("kD_mode6", source="15", width=200)
        add_input_text("pow_mode6", source="16", width=200)
        add_button("Set params", callback=plot_callback)
        add_button("Save params", callback=test)

    add_same_line()
    '''
    with group("Right Panel", width=250):
        add_button("Z", callback=plot_callback)
        add_input_text("New Tdfgdfg", source="new-tdfgdfg", width=200)
    '''
    add_same_line()
    add_plot("Plot", height=-1)

def render_call():
    global gl
    gl += 0.1
    plot_callback()

set_render_callback(render_call)
start_dearpygui(primary_window="Main Window")

