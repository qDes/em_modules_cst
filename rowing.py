import datetime
import json

from dearpygui.core import *
from dearpygui.simple import *
import pyscreenshot as ImageGrab

from util_ import UDP, Plotter, PlotSaver

#ROOT_DIR = "/home/lar/Desktop"
ROOT_DIR = "/Users/a18351639/projects"
PARAMS = f"{ROOT_DIR}/em_modules_cst/params/rowing.json"
HELP = f"{ROOT_DIR}/em_modules_cst/params/rowing.help"
RECORD_DIR = f"{ROOT_DIR}/em_modules_cst/plots"


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
        y1, y2, y3, y4 = y[0], y[1], y[5], y[6]
        plot.update(get_delta_time(), y1, y2, y3, y4)
        # clear_plot("Plot")
        add_line_series("Plot", "F0", plot.x1, plot.y1, weight=2, axis=0)
        add_line_series("Plot", "pos0", plot.x2, plot.y2, weight=2, axis=1)
        add_line_series("Plot1", "F1", plot.x3, plot.y3, weight=2, axis=0)
        add_line_series("Plot1", "pos1", plot.x4, plot.y4, weight=2, axis=1)

        add_line_series("Plot2", name='Power1, W', x=plot.px, y=plot.p1, weight=2, axis=0)
        add_line_series("Plot2", name='Power2, W', x=plot.px, y=plot.p2, weight=2, axis=0)
        print(len(plot.p1), len(plot.p2), len(plot.px))

        if recorder.is_saving:
            recorder.get_data(y1, y2, y3, y4)


def save_params(sender, data):
    i0, a, b, c, d, e, f, m_inner, kOut_mode0, kOut_mode1 = get_data("", "")
    params = dict(i0=i0, a=a, b=b, c=c, d=d, e=e, f=f, m_inner=m_inner, kOut_mode0=kOut_mode0, kOut_mode1=kOut_mode1)
    with open(PARAMS, "w") as my_file:
        my_file.write(json.dumps(params))


def load_params(sender, data):
    with open(PARAMS, "r") as my_file:
        data = json.loads(my_file.read())
    set_value("i0", data['i0'])
    set_value("a", data['a'])
    set_value("b", data['b'])
    set_value("c", data['c'])
    set_value("d", data['d'])
    set_value("e", data['f'])
    set_value("f", data['f'])
    set_value("m_inner", data['m_inner'])
    set_value("kOut_mode0", data['kOut_mode0'])
    set_value("kOut_mode1", data['kOut_mode1'])


def close_help():
    close_popup("Help Popup")


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
        f"{ROOT_DIR}/em_modules_cst/screenshots/rowing_{datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S')}.png")


def set_plot_time():
    clear_plot("Plot")
    plot_len = int(get_value("plot_time")) * 50
    plot.update_limit(plot_len)
    plot.lim = plot_len


with window("Main Window"):
    with group("Left Panel", width=250):
        # add_button("Plot data", callback=plot_callback)
        add_text("Connection parameters")

        # add_input_text("Address", source="address", default_value="192.168.0.193", width=200)
        add_input_text("Address", source="address", default_value="192.168.31.149", width=200)
        add_button("Connect", callback=connect)
        add_button("Disconnect", callback=disconnect)
        ## Params
        add_text("Model parameters")
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
        with tab("Plot 3"):
            add_plot("Plot2", height=-1, yaxis2=True, x_axis_name="Training time, s")

if __name__ == "__main__":
    i0, a, b, c, d, e, f, m_inner, kOut_mode0, kOut_mode1 = get_data("", "")
    plot = Plotter()
    udp = UDP(i0, a, b, c, d, e, f, m_inner, kOut_mode0, kOut_mode1)
    recorder = PlotSaver(RECORD_DIR, "rowing")
    set_main_window_title("Rowing")
    set_render_callback(render_call)
    start_dearpygui(primary_window="Main Window")
