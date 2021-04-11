from dearpygui.core import *
from dearpygui.simple import *

from util_ import UDP
from util import connect, disconnect, Plotter

def setup_params(sender, data):
    i0, jam_pos_in, F_set, kShaker, shaker_freq, m, f_mode2, f_mode3, a_mode5, b_mode5, c_mode5, d_mode5, g_mode5, v_mode6, kD_mode6, pow_mode6 = get_data(
        "", "")
    udp.update_params(i0, jam_pos_in, F_set, kShaker, shaker_freq, m, f_mode2, f_mode3, a_mode5, b_mode5, c_mode5,
                      d_mode5, g_mode5, v_mode6, kD_mode6, pow_mode6)
def render_call(sender, data):
    pass


with window("Main Window"):
    with group("Left Panel", width=250):
        # add_button("Plot data", callback=plot_callback)
        add_text("Connection params")
        add_input_text("Address", source="address", default_value="192.168.0.193", width=200)
        # add_input_text("Port", source="port", default_value="1234", width=200)
        add_button("Connect", callback=connect)
        add_button("Disconnect", callback=disconnect)
        ## Params
        add_text("Model params")
        add_listbox("mode", source="i0", default_value=0, items=["0", "1", "2"])
        add_input_text("a", source="a", default_value="0.1", width=200)
        add_input_text("b", source="b", default_value="10.0", width=200)
        add_input_text("c", source="c", default_value="0.1", width=200)
        add_input_text("d", source="d", default_value="0.1", width=200)
        add_input_text("e", source="e", default_value="20.0", width=200)
        add_input_text("f", source="f", default_value="0.0", width=200)
        add_input_text("kOut_mode0", source="kOut_mode0", default_value="1.0", width=200)
        add_input_text("kOut_mode1", source="kOut_mode1", default_value="0.0", width=200)

        add_button("Set params", callback=setup_params)
        # add_button("Save params", callback=test)

    add_same_line()
    with group("Right Panel"):
        add_same_line()
        add_plot("Plot0", height=-1, x_axis_name="Counter", y_axis_name="F, pos")
    add_same_line()
    add_plot("Plot1", height=-1, x_axis_name="Counter", y_axis_name="F, pos")


if __name__ == "__main__":
    plot = Plotter()
    udp = UDP()

    set_render_callback(render_call)
    start_dearpygui(primary_window="Main Window")
