import json
from dearpygui.core import *
from dearpygui.simple import *

from util_ import UDP, Plotter

PARAMS = "/Users/a18351639/projects/em_modules_cst/params/main.json"
HELP = "/Users/a18351639/projects/em_modules_cst/params/main.help"


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
    i0, jam_pos_in, F_set, kShaker, shaker_freq, m, f_mode2, f_mode3, a_mode5, b_mode5, c_mode5, d_mode5, g_mode5, v_mode6, kD_mode6, pow_mode6 = get_data(
        "", "")

    udp.update_params(i0, jam_pos_in, F_set, kShaker, shaker_freq, m, f_mode2, f_mode3, a_mode5, b_mode5, c_mode5,
                      d_mode5, g_mode5, v_mode6, kD_mode6, pow_mode6)


def get_data(sender, data):
    i0 = int(get_value("i0"))
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

    return i0, jam_pos_in, F_set, kShaker, shaker_freq, m, f_mode2, f_mode3, a_mode5, b_mode5, c_mode5, d_mode5, g_mode5, v_mode6, kD_mode6, pow_mode6


def plot_callback():
    global udp, plot
    if udp.enable:
        x = udp.send()
        if not x:
            return
        x1, x2 = x[3], x[4]
        plot.update(x1, x2)
        clear_plot("Plot")
        add_line_series("Plot", "F", plot.x1, plot.y1, weight=2)
        add_line_series("Plot", "pos", plot.x2, plot.y2, weight=2)


def save_params(sender, data):
    i0, jam_pos_in, F_set, kShaker, shaker_freq, m, \
    f_mode2, f_mode3, a_mode5, b_mode5, c_mode5, d_mode5, g_mode5, v_mode6, kD_mode6, pow_mode6 = get_data("", "")
    params = dict(i0=i0, jam_pos_in=jam_pos_in, F_set=F_set, kShaker=kShaker, shaker_freq=shaker_freq, m=m,
                  f_mode2=f_mode2, f_mode3=f_mode3, a_mode5=a_mode5, b_mode5=b_mode5, c_mode5=c_mode5, d_mode5=d_mode5,
                  g_mode5=g_mode5, v_mode6=v_mode6, kD_mode6=kD_mode6, pow_mode6=pow_mode6)
    with open(PARAMS, "w") as my_file:
        my_file.write(json.dumps(params))


def close_help():
    close_popup("Help Popup")


def load_params(sender, data):
    with open(PARAMS, "r") as my_file:
        data = json.loads(my_file.read())
    set_value("i0", data['i0'])
    set_value("jam_pos_in", data["jam_pos_in"])
    set_value("F_set", data["F_set"])
    set_value("kShaker", data["kShaker"])
    set_value("shaker_freq", data["shaker_freq"])
    set_value("m", data["m"])
    set_value("f_mode2", data["f_mode2"])
    set_value("f_mode3", data["f_mode3"])
    set_value("a_mode5", data["a_mode5"])
    set_value("b_mode5", data["b_mode5"])
    set_value("c_mode5", data["c_mode5"])
    set_value("d_mode5", data["d_mode5"])
    set_value("g_mode5", data["g_mode5"])
    set_value("v_mode6", data["v_mode6"])
    set_value("kD_mode6", data["kD_mode6"])
    set_value("pow_mode6", data["pow_mode6"])


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
        add_listbox("mode", source="i0", default_value=0, items=["0", "1", "2", "3", "4", "5", "6", "7", "8"])
        add_input_text("jam_pos_in", source="jam_pos_in", default_value="0.1", width=200)
        add_input_text("F_set", source="F_set", default_value="10.0", width=200)
        add_input_text("kShaker", source="kShaker", default_value="0.1", width=200)
        add_input_text("shaker_freq", source="shaker_freq", default_value="0.1", width=200)
        add_input_text("m", source="m", default_value="20.0", width=200)
        add_input_text("f_mode2", source="f_mode2", default_value="0.0", width=200)
        add_input_text("f_mode3", source="f_mode3", default_value="1.0", width=200)
        # add_input_text("F_set_", source="F_set_", width=200)
        add_input_text("a_mode5", source="a_mode5", default_value="0.0", width=200)
        add_input_text("b_mode5", source="b_mode5", default_value="0.0", width=200)
        add_input_text("c_mode5", source="c_mode5", default_value="0.0", width=200)
        add_input_text("d_mode5", source="d_mode5", default_value="0.0", width=200)
        add_input_text("g_mode5", source="g_mode5", default_value="0.0", width=200)
        add_input_text("v_mode6", source="v_mode6", default_value="0.0", width=200)
        add_input_text("kD_mode6", source="kD_mode6", default_value="0.0", width=200)
        add_input_text("pow_mode6", source="pow_mode6", default_value="2", width=200)

        add_button("Set params", callback=setup_params)
        add_spacing(count=10)
        add_button("Save params", callback=save_params)
        add_button("Load params", callback=load_params)
        add_button("Help")

        with popup("Help", 'Help Popup', modal=True, mousebutton=mvMouseButton_Left):
            with open(HELP, 'r') as my_file:
                help_data = my_file.read()
            add_text(help_data)
            add_button("Close", callback=close_help)

    add_same_line()
    add_plot("Plot", height=-1, x_axis_name="Counter", y_axis_name="F, pos")


def render_call(sender, data):
    plot_callback()


if __name__ == "__main__":
    i0, jam_pos_in, F_set, kShaker, shaker_freq, m, f_mode2, f_mode3, a_mode5, b_mode5, c_mode5, d_mode5, g_mode5, v_mode6, kD_mode6, pow_mode6 = get_data(
        "", "")
    udp = UDP(i0, jam_pos_in, F_set, kShaker, shaker_freq, m, f_mode2, f_mode3, a_mode5, b_mode5, c_mode5, d_mode5,
              g_mode5, v_mode6, kD_mode6, pow_mode6)
    plot = Plotter()
    set_main_window_title("Universal/Inclided")
    set_render_callback(render_call)
    start_dearpygui(primary_window="Main Window")
