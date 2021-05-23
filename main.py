import datetime
import json

from dearpygui.core import *
from dearpygui.simple import *
import pyscreenshot as ImageGrab

from util_ import UDP, Plotter, PlotSaver

# ROOT_DIR = "/home/lar/Desktop"
ROOT_DIR = "/Users/a18351639/projects"
PARAMS = f"{ROOT_DIR}/em_modules_cst/params/main.json"
HELP = f"{ROOT_DIR}/em_modules_cst/params/main.help"
RECORD_DIR = f"{ROOT_DIR}/em_modules_cst/plots"

COUNTER = 0


def connect(sender, data):
    global udp
    configure_item("Address", enabled=False)
    udp.enable = True
    address = get_value("address")
    # port = get_value("port")
    udp.connect(address)
    print(address)


def disconnect(sender, data):
    global udp
    configure_item("Address", enabled=True)
    udp.enable = False


def setup_params(sender, data):
    i0, jam_pos_in, F_set, kShaker, shaker_freq, m, f_mode2, f_mode3, a_mode5, b_mode5, c_mode5, d_mode5, g_mode5, v_mode6, kD_mode6, pow_mode6 = get_data(
        "", "")
    print(i0, jam_pos_in, F_set, kShaker, shaker_freq, m, f_mode2, f_mode3, a_mode5, b_mode5, c_mode5, d_mode5, g_mode5,
          v_mode6, kD_mode6, pow_mode6)
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
    global udp, plot, COUNTER
    '''
    COUNTER += 1

    if COUNTER % 3 != 0:
        print(COUNTER)
        return
    '''
    if udp.enable:
        y = udp.send()
        if not y:
            return
        y1, y2 = y[0], y[1]
        y2 *= 100
        plot.update(get_delta_time(), y1, y2)

        # clear_plot("Plot1")

        add_line_series("Plot", "Force, N", plot.x1, plot.y1, weight=2, axis=0)
        add_line_series("Plot", "Position, cm", plot.x2, plot.y2, weight=2, axis=1)

        add_line_series("Plot", name='', x=plot.x2, y=[0 for x in plot.x2], weight=0, axis=0)
        add_line_series("Plot", name='', x=plot.x2, y=[600 for x in plot.x2], weight=0, axis=0)
        add_line_series("Plot", name='', x=plot.x2, y=[-1 for x in plot.x2], weight=0, axis=1)
        add_line_series("Plot", name='', x=plot.x2, y=[100 for x in plot.x2], weight=0, axis=1)

        add_line_series("Plot1", name='Power, W', x=plot.px, y=plot.p1, weight=2, axis=0)
        # add_line_series("Plot1", name=f'Total power {plot.total_power_0}, W', x=plot.px, y=[0 for x in plot.px], weight=0, axis=0)

        if recorder.is_saving:
            recorder.get_data(y1, y2)


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


def start_record():
    configure_item("Start record", enabled=False)
    recorder.start()


def stop_record():
    configure_item("Start record", enabled=True)
    recorder.stop()


def make_screenshot():
    # grab fullscreen
    im = ImageGrab.grab()

    # save image file
    im.save(
        f"{ROOT_DIR}/em_modules_cst/screenshots/main_{datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S')}.png")


def set_plot_time():
    clear_plot("Plot")
    plot_len = int(get_value("plot_time")) * 50
    plot.update_limit(plot_len)
    plot.lim = plot_len


with window("Main Window"):
    with group("Left Panel", width=250):
        # add_button("Plot data", callback=plot_callback)
        add_text("Connection params")
        # add_input_text("Address", source="address", default_value="192.168.0.193", width=200)
        add_input_text("Address", source="address", default_value="192.168.31.149", width=200)
        # add_input_text("Port", source="port", default_value="1234", width=200)
        add_button("Connect", callback=connect)
        add_button("Disconnect", callback=disconnect)
        ## Params
        add_text("Model parameters")
        add_listbox("mode", source="i0", default_value=0, items=["0. Disabled",
                                                                 "1. Constant position with vibration",
                                                                 "2. Mass mode",
                                                                 "3. Constant velocity",
                                                                 "4. Overpowering mode",
                                                                 "5. Friction mode",
                                                                 "6. User mode",
                                                                 "7. Viscosity",
                                                                 "8. Mass mode InerciaFree"])
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

        add_button("Set parameters", callback=setup_params)
        add_spacing(count=3)
        add_button("Save parameters", callback=save_params)
        add_button("Load parameters", callback=load_params)
        add_spacing(count=3)
        add_button("Start record", callback=start_record)
        add_button("Stop record", callback=stop_record)
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
    with tab_bar("Plots"):
        with tab("Plot 1"):
            add_plot("Plot", height=-1, yaxis2=True, x_axis_name="Training time, s")
        with tab("Plot 2"):
            add_plot("Plot1", height=-1, yaxis2=True, x_axis_name="Training time, s")

click_check = False


def render_call(sender, data):
    global click_check
    plot_callback()

    if is_item_clicked("mode"):
        click_check = True
        return
    if click_check:
        print(get_value("i0"))
        click_check = False


if __name__ == "__main__":
    i0, jam_pos_in, F_set, kShaker, shaker_freq, m, f_mode2, f_mode3, a_mode5, b_mode5, c_mode5, d_mode5, g_mode5, v_mode6, kD_mode6, pow_mode6 = get_data(
        "", "")
    udp = UDP(i0, jam_pos_in, F_set, kShaker, shaker_freq, m, f_mode2, f_mode3, a_mode5, b_mode5, c_mode5, d_mode5,
              g_mode5, v_mode6, kD_mode6, pow_mode6)
    plot = Plotter()
    recorder = PlotSaver(RECORD_DIR, "main")
    set_main_window_title("Universal/Inclided")
    # add_line_series("Plot", name='', x=[0, 10], y=[0, 0], weight=0, axis=0)
    # add_line_series("Plot", name='', x=[0, 1], y=[600, 600], weight=0, axis=0)
    # add_line_series("Plot", name='', x=[0, 1], y=[-1, -1], weight=0, axis=1)
    # add_line_series("Plot", name='', x=[0, 1], y=[100, 100], weight=0, axis=1)
    set_render_callback(render_call)

    start_dearpygui(primary_window="Main Window")
