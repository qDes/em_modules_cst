from dearpygui.core import *
from dearpygui.simple import *

from util_ import UDP
from util import Plotter


def connect(sender, data):
    global udp
    udp.enable = True
    address = get_value("address")
    # port = get_value("port")
    udp.connect(address)
    print(address)


def disconnect(sender, data):
    global udp
    udp.enable = False


def setup_params(sender, data):
    i0, a, b, c, d, e, f, m_inner, kOut_mode0, kOut_mode1 = get_data(
        "", "")
    udp.update_params(i0, a, b, c, d, e, f, m_inner, kOut_mode0, kOut_mode1)


def get_data(sender, data):
    i0 = int(get_value("i0"))
    a = float(get_value("a"))
    b = float(get_value("b"))
    c = float(get_value("c"))
    d = float(get_value("d"))
    e = float(get_value("e"))
    f = float(get_value("f"))
    m_inner = float(get_value("m_inner"))
    kOut_mode0 = float(get_value("kOut_mode0"))
    kOut_mode1 = float(get_value("kOut_mode1"))
    print(i0, a, b, c, d, e, f, m_inner, kOut_mode0, kOut_mode1)
    return i0, a, b, c, d, e, f, m_inner, kOut_mode0, kOut_mode1


def render_call(sender, data):
    plot_callback()


def plot_callback():
    global udp, plot
    if udp.enable:
        y = udp.send()
        if not y:
            return
        y1, y2, y3, y4 = y[3], y[4], y[6], y[7]
        plot.update(y1, y2, y3, y4)
        clear_plot("Plot")
        add_line_series("Plot", "F0", plot.x1, plot.y1, weight=2)
        add_line_series("Plot", "pos0", plot.x2, plot.y2, weight=2)
        add_line_series("Plot", "F1", plot.x1, plot.y1, weight=2)
        add_line_series("Plot", "pos1", plot.x2, plot.y2, weight=2)


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
        add_input_text("f, m", source="f", default_value="0.0", width=200)
        add_input_text("m_inner, kg", source="m_inner", default_value="5.0", width=200)
        add_input_text("kOut_mode0", source="kOut_mode0", default_value="1.0", width=200)
        add_input_text("kOut_mode1", source="kOut_mode1", default_value="0.0", width=200)

        add_button("Set params", callback=setup_params)
        # add_button("Save params", callback=test)

    add_same_line()
    add_plot("Plot", height=-1, x_axis_name="Counter", y_axis_name="F0, pos0, F1, pos1")

if __name__ == "__main__":
    i0, a, b, c, d, e, f, m_inner, kOut_mode0, kOut_mode1 = get_data("", "")
    plot = Plotter()
    udp = UDP(i0, a, b, c, d, e, f, m_inner, kOut_mode0, kOut_mode1)

    set_main_window_title("Rowing")
    set_render_callback(render_call)
    start_dearpygui(primary_window="Main Window")