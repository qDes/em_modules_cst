import datetime
import json
import os

from dearpygui.core import *
from dearpygui.simple import *
import pyscreenshot as ImageGrab

from util_ import Plotter, UDP, PlotSaver, disable_items, enable_items, close_help, disable_readonly

ROOT_DIR = os.getcwd()
PARAMS = f"{ROOT_DIR}/params/velo.json"
HELP = f"{ROOT_DIR}/params/velo.help"
RECORD_DIR = f"{ROOT_DIR}/plots"

POST_CONNECTION_COMMON_ITEMS = ["Disconnect", "mode", "Set parameters", "Save parameters", "Load parameters",
                                "Start record", "Stop record", "Autocalib"]  # , "Set plot time", "s"]
MODEL_PARAMS = ["m_inner, kg", "friction, N", "kPedal", "calib", "kShaker", "Shaker_limit, m", "F_set, N",
                "shaker_freqp, Hz", "p_set, deg."]


def connect(sender, data):
    global udp
    udp.enable = True
    address = get_value("address")
    # port = get_value("port")
    udp.connect(address)
    print(address)
    enable_items(POST_CONNECTION_COMMON_ITEMS)
    disable_items(["Connect", "Address"])
    disable_readonly(MODEL_PARAMS)
    disable_readonly(["s"])


def disconnect(sender, data):
    global udp
    udp.enable = False


def setup_params(sender, data):
    i0, p_set, friction, kShaker, shaker_limit, F_set, shaker_freqp, m_inner, kPedal, calib = get_data("", "")
    udp.update_params(i0, p_set, friction, kShaker, shaker_limit, F_set, shaker_freqp, m_inner, kPedal, calib)


def another_pedal(x):
    x += 180
    if x > 180:
        return x % 180
    return x


def plot_callback():
    global udp, plot
    if udp.enable:
        x = udp.send()
        if not x:
            return
        x1, x2 = x[0], x[1]
        x2 = x2 % 360 - 180
        x3 = x2 % 360 - 180
        plot.update(get_delta_time(), x1, x2, x3)

        # add_line_series("Force", name='', x=plot.x2, y=[0 for x in plot.x2], weight=0, axis=0)
        # add_line_series("Force", name='', x=plot.x2, y=[1500 for x in plot.x2], weight=0, axis=0)
        # add_line_series("Plot", name='', x=plot.x2, y=[-1 for x in plot.x2], weight=0, axis=1)
        # add_line_series("Plot", name='', x=plot.x2, y=[100 for x in plot.x2], weight=0, axis=1)
        # clear_plot("Plot")

        add_line_series("Force", "F, N", plot.x1, plot.y1, weight=2, axis=0, color=[255, 0, 0])
        # TODO: добавить границы -180 180
        add_line_series("Pedal Angle", "angle left, deg", plot.x2, plot.y2, weight=2, axis=0)
        add_line_series("Pedal Angle", "angle right, deg", plot.x2, plot.y3, weight=2, axis=0)
        add_line_series("Pedal Angle", name='', x=plot.x2, y=[-180 for x in plot.x2], weight=0, axis=0)
        add_line_series("Pedal Angle", name='', x=plot.x2, y=[180 for x in plot.x2], weight=0, axis=0)
        # multiple by l - length of velo rod due to get moment
        l = 0.25
        add_line_series("Power", name='Power, W', x=plot.px, y=[y * l for y in plot.p1], weight=2, axis=0,
                        color=[255, 0, 0, -1])

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
    m_inner = get_value("m_inner")
    print(m_inner)
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


def render_call(sender, data):
    global udp

    if not udp.enable:
        enable_items(["Connect", "Address"])
        disable_items(POST_CONNECTION_COMMON_ITEMS + MODEL_PARAMS)
        set_value("i0", 0)
        setup_params("", "")
    plot_callback()


def start_record():
    configure_item("Start record", enabled=False)
    recorder.start("F, N; angle, deg; timestamp")


def stop_record():
    configure_item("Start record", enabled=True)
    recorder.stop()


def make_screenshot():
    # grab fullscreen
    im = ImageGrab.grab()

    # save image file
    im.save(f"{ROOT_DIR}/screenshots/velo_{datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S')}.png")


def set_plot_time():
    clear_plot("Force")
    plot_len = int(get_value("plot_time")) * 50
    plot.update_limit(plot_len)
    plot.lim = plot_len


def select_mode():
    mode = int(get_value("i0"))
    if mode == 0:
        disable_items(MODEL_PARAMS)
    elif mode == 1:
        disable_items(MODEL_PARAMS)
        enable_items(MODEL_PARAMS[:4])
        disable_readonly(MODEL_PARAMS[:4])
    elif mode == 2:
        enable_items(MODEL_PARAMS)
        disable_readonly(MODEL_PARAMS)


def setup_calib():
    set_value("calib", -1*plot.y1[-1])


with window("Main Window"):
    with group("Left Panel", width=250):
        add_text("Connection parameters")
        add_input_text("Address", source="address", default_value="192.168.0.193", width=200)
        # add_input_text("Address", source="address", default_value="192.168.0.168", width=200)
        add_button("Connect", callback=connect)
        add_button("Disconnect", callback=disconnect, enabled=False)
        ## Params
        add_text("Model parameters")
        add_listbox("mode", source="i0", default_value=0, items=["0. Off", "1. Manual", "2. Vibration"], enabled=False,
                    num_items=3,
                    callback=select_mode)
        add_slider_float("p_set, deg.", source="p_set", default_value=0.0, width=200, enabled=False, min_value=0.0,
                         max_value=270.0, step=1.0)
        add_input_float("friction, N", source="friction", default_value=50.0, width=200, enabled=False, step=1.0)
        add_input_float("kShaker", source="kShaker", default_value=0.1, width=200, enabled=False)
        add_input_float("Shaker_limit, m", source="shaker_limit", default_value=0.1, width=200, enabled=False)
        add_input_float("F_set, N", source="F_set", default_value=0.0, width=200, enabled=False, step=1.0)
        add_slider_float("shaker_freqp, Hz", source="shaker_freqp", default_value=1.0, width=200, enabled=False,
                         min_value=1.0, max_value=100.0)
        add_input_float("m_inner, kg", source="m_inner", default_value=60.0, width=200, enabled=False, step=1.0)
        add_input_float("kPedal", source="kPedal", default_value=1.0, width=200, enabled=False)
        add_input_float("calib", source="calib", default_value=0.0, width=200, enabled=False)

        add_button("Set parameters", callback=setup_params, enabled=False)
        add_spacing(count=3)
        add_button("Autocalib", callback=setup_calib, enabled=False)
        add_spacing(count=3)
        add_button("Save parameters", callback=save_params, enabled=False)
        add_button("Load parameters", callback=load_params, enabled=False)
        add_spacing(count=3)
        add_button("Start record", callback=start_record, enabled=False)
        add_button("Stop record", callback=stop_record, enabled=False)
        add_spacing(count=3)
        add_button("Help")
        add_spacing(count=3)
        add_button("Screenshot", callback=make_screenshot)
        add_spacing(count=3)
        add_input_text("s", source="plot_time", default_value="10", width=50)
        add_button("Set plot time", callback=set_plot_time)
        with popup("Help", 'Help Popup', modal=True, mousebutton=mvMouseButton_Left):
            with open(HELP, 'r') as my_file:
                help_data = my_file.read()
            add_text(help_data)
            add_button("Close", callback=close_help)

    add_same_line()
    '''
    with tab_bar("Plots"):
        with tab("Plot 1"):
            add_plot("Plot", height=-1, yaxis2=True, x_axis_name="Training time, s")
        with tab("Plot 2"):
            add_plot("Plot1", height=-1, yaxis2=True, x_axis_name="Training time, s")
    '''
    with tab_bar("Plots"):
        with tab("Plot 1"):
            add_plot("Force", x_axis_name="Training time, s", height=250)
            add_plot("Pedal Angle", x_axis_name="Training time, s", height=250)
            add_plot("Power", x_axis_name="Training time, s", height=250)

if __name__ == "__main__":
    i0, p_set, friction, kShaker, shaker_limit, F_set, shaker_freqp, m_inner, kPedal, calib = get_data("", "")
    udp = UDP(i0, p_set, friction, kShaker, shaker_limit, F_set, shaker_freqp, m_inner, kPedal, calib)
    plot = Plotter()
    recorder = PlotSaver(RECORD_DIR, "velo")
    set_main_window_title("Velo")
    set_render_callback(render_call)
    start_dearpygui(primary_window="Main Window")
