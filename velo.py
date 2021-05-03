import json

from dearpygui.core import *
from dearpygui.simple import *

from util_ import Plotter, UDP, PlotSaver

PARAMS = "/Users/a18351639/projects/em_modules_cst/params/velo.json"
HELP = "/Users/a18351639/projects/em_modules_cst/params/velo.help"
RECORD_DIR = "/Users/a18351639/projects/em_modules_cst/plots"


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
    i0, p_set, friction, kShaker, shaker_limit, F_set, shaker_freqp, m_inner, kPedal, calib = get_data("", "")
    udp.update_params(i0, p_set, friction, kShaker, shaker_limit, F_set, shaker_freqp, m_inner, kPedal, calib)


def render_call(sender, data):
    plot_callback()


def plot_callback():
    global udp, plot
    if udp.enable:
        x = udp.send()
        if not x:
            return
        x1, x2 = x[0], x[1]
        plot.update(x1, x2)
        clear_plot("Plot")
        add_line_series("Plot", "F", plot.x1, plot.y1, weight=2, axis=0)
        add_line_series("Plot", "angle", plot.x2, plot.y2, weight=2, axis=1)
        if recorder.is_saving:
            recorder.get_data(x1, x2)


def get_data(sender, data):
    i0 = int(get_value("i0"))
    p_set = float(get_value("p_set"))
    friction = float(get_value("friction"))
    kShaker = float(get_value("kShaker"))
    shaker_limit = float(get_value("shaker_limit"))
    F_set = float(get_value("F_set"))
    shaker_freqp = float(get_value("shaker_freqp"))
    m_inner = float(get_value("m_inner"))
    kPedal = float(get_value("kPedal"))
    calib = float(get_value("calib"))
    print(i0, p_set, friction, kShaker, shaker_limit, F_set, shaker_freqp, m_inner, kPedal, calib)
    return i0, p_set, friction, kShaker, shaker_limit, F_set, shaker_freqp, m_inner, kPedal, calib


def save_params(sender, data):
    i0, p_set, friction, kShaker, shaker_limit, F_set, shaker_freqp, m_inner, kPedal, calib = get_data("", "")
    params = dict(i0=i0, p_set=p_set, friction=friction, kShaker=kShaker, shaker_limit=shaker_limit, F_set=F_set,
                  shaker_freqp=shaker_freqp, m_inner=m_inner, kPedal=kPedal, calib=calib)
    with open(PARAMS, "w") as my_file:
        my_file.write(json.dumps(params))


def load_params(sender, data):
    with open(PARAMS, "r") as my_file:
        data = json.loads(my_file.read())
    set_value("i0", data['i0'])
    set_value("p_set", data['p_set'])
    set_value("friction", data['friction'])
    set_value("kShaker", data['kShaker'])
    set_value("shaker_limit", data['shaker_limit'])
    set_value("F_set", data['F_set'])
    set_value("shaker_freqp", data['shaker_freqp'])
    set_value("m_inner", data['m_inner'])
    set_value("kPedal", data['kPedal'])
    set_value("calib", data['calib'])


def close_help():
    close_popup("Help Popup")


def start_record():
    recorder.start()


def stop_record():
    recorder.stop()


with window("Main Window"):
    with group("Left Panel", width=250):
        add_text("Connection params")
        add_input_text("Address", source="address", default_value="192.168.0.193", width=200)
        #add_input_text("Address", source="address", default_value="192.168.31.149", width=200)
        add_button("Connect", callback=connect)
        add_button("Disconnect", callback=disconnect)
        ## Params
        add_text("Model params")
        add_listbox("mode", source="i0", default_value=0, items=["0", "1", "2"])
        add_input_text("p_set, deg.", source="p_set", default_value="0.1", width=200)
        add_input_text("friction, N", source="friction", default_value="10.0", width=200)
        add_input_text("kShaker", source="kShaker", default_value="0.1", width=200)
        add_input_text("Shaker_limit, m", source="shaker_limit", default_value="0.1", width=200)
        add_input_text("F_set, N", source="F_set", default_value="20.0", width=200)
        add_input_text("shaker_freqp, Hz", source="shaker_freqp", default_value="1.0", width=200)
        add_input_text("m_inner, kg", source="m_inner", default_value="1.0", width=200)
        add_input_text("kPedal", source="kPedal", default_value="0.0", width=200)
        add_input_text("calib", source="calib", default_value="0.0", width=200)

        add_button("Set params", callback=setup_params)
        add_spacing(count=10)
        add_button("Save params", callback=save_params)
        add_button("Load params", callback=load_params)
        add_spacing(count=10)
        add_button("Start record", callback=start_record)
        add_button("Stop record", callback=stop_record)
        add_spacing(count=10)
        add_button("Help")

        with popup("Help", 'Help Popup', modal=True, mousebutton=mvMouseButton_Left):
            with open(HELP, 'r') as my_file:
                help_data = my_file.read()
            add_text(help_data)
            add_button("Close", callback=close_help)

    add_same_line()

    add_plot("Plot", height=-1, x_axis_name="Counter", y_axis_name="F, angle", yaxis2=True)

if __name__ == "__main__":
    i0, p_set, friction, kShaker, shaker_limit, F_set, shaker_freqp, m_inner, kPedal, calib = get_data("", "")
    udp = UDP(i0, p_set, friction, kShaker, shaker_limit, F_set, shaker_freqp, m_inner, kPedal, calib)
    plot = Plotter()
    recorder = PlotSaver(RECORD_DIR, "velo")
    set_main_window_title("Velo")
    set_render_callback(render_call)
    start_dearpygui(primary_window="Main Window")
