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

def connection(sender, data):
    address = get_value("address")
    port = get_value("port")
    print(address, port)

def get_data(sender, data):
    jam_pos_in = float(get_value("jam_pos_in"))
    F_set = float(get_value("F_set"))
    kShaker = float(get_value("kShaker"))
    shaker_freq = float(get_value("shaker_freq"))
    m = float(get_value("m"))
    f_mode2 = float(get_value("f_mode2"))
    f_mode3 = float(get_value("f_mode3"))
    a_mode5 = float(get_value("a_mode5"))
    b_mode5 = float(get_value("b_mode5"))
    c_mode5 = float(get_value("c_mode5"))
    d_mode5 = float(get_value("d_mode5"))
    g_mode5 = float(get_value("g_mode5"))
    v_mode6 = float(get_value("v_mode6"))
    kD_mode6 = float(get_value("kD_mode6"))
    pow_mode6 = float(get_value("pow_mode6"))

    print(jam_pos_in, F_set, kShaker, shaker_freq, m, f_mode2, f_mode3, a_mode5, b_mode5,
          c_mode5, d_mode5, g_mode5, v_mode6, kD_mode6, pow_mode6)


with window("Main Window"):
    with group("Left Panel", width=250):
        # add_button("Plot data", callback=plot_callback)
        add_text("Connection params")
        add_input_text("Address", source="address", default_value="0.0.0.0", width=200)
        add_input_text("Port", source="port", default_value="1234", width=200)
        add_button("Connect", callback=connection)
        ## Params
        add_text("Model params")
        add_input_text("jam_pos_in", source="jam_pos_in", default_value="0.1",  width=200)
        add_input_text("F_set", source="F_set", default_value="10.0", width=200)
        add_input_text("shaker_amp", source="shaker_freq", default_value="0.1", width=200)
        add_input_text("kShaker", source="kShaker", default_value="0.1", width=200)
        add_input_text("m", source="m", default_value="20.0", width=200)
        add_input_text("f_mode2", source="f_mode2", default_value="0.0", width=200)
        add_input_text("f_mode3", source="f_mode3", default_value="1.0", width=200)
        #add_input_text("F_set_", source="F_set_", width=200)
        add_input_text("a_mode5", source="a_mode5", default_value="0.0", width=200)
        add_input_text("b_mode5", source="b_mode5", default_value="0.0", width=200)
        add_input_text("c_mode5", source="c_mode5", default_value="0.0", width=200)
        add_input_text("d_mode5", source="d_mode5", default_value="0.0", width=200)
        add_input_text("g_mode5", source="g_mode5", default_value="0.0", width=200)
        add_input_text("v_mode6", source="v_mode6", default_value="0.0", width=200)
        add_input_text("kD_mode6", source="kD_mode6", default_value="0.0", width=200)
        add_input_text("pow_mode6", source="pow_mode6", default_value="2", width=200)

        add_button("Set params", callback=get_data)
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
