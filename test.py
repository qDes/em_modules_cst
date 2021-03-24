from dearpygui.core import *
from dearpygui.simple import *
from math import pi, sin, cos
from datetime import datetime

import threading
from time import sleep

# Simple analog clock - https://gitlab.com/-/snippets/2077355

W = H = 300
MAIN_WINDOW = 'DPG Clock'
BGCOLOR = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 192, 0)
YELLOW = (255, 255, 0)
RING_COLOR = BLUE
HCOLOR = RED
MCOLOR = DARK_GREEN
SCOLOR = YELLOW

class Test:

    def __init__(self):
        self.counter = 0
        self._lock = threading.Lock()

    def update(self):
        with self._lock:
            self.counter += 1


test = Test()

def add_simple_clock(parent, size, center):
    draw_rectangle(parent, (0, 0), (W, H), BGCOLOR,
                   fill=BGCOLOR, tag='bg')
    draw_circle(parent, center, int(.45 * size),
                RING_COLOR, segments=1200, thickness=5, tag='cir')
    add_data("lastUpdate", datetime.now().second)
    add_data("clockSize", size)
    add_data("parent", parent)
    now = datetime.now()
    mi = now.minute  # + se / 60
    ho = now.hour % 12 + mi / 60
    se = now.second
    r0 = size // 2

    angle = -pi / 2 + pi * ho / 6
    c, s = cos(angle), sin(angle)
    l = size * .225
    draw_line(parent, (r0 + 7 * c, r0 + 7 * s), (r0 + l * c, r0 + l * s),
              HCOLOR, 6, tag="hour")

    angle = -pi / 2 + pi * mi / 30
    l = size * .4
    c, s = cos(angle), sin(angle)
    draw_line(parent, (r0 + 7 * c, r0 + 7 * s), (r0 + l * c, r0 + l * s),
              MCOLOR, 4, tag="minute")

    angle = -pi / 2 + pi * se / 30
    c, s = cos(angle), sin(angle)
    draw_line(parent, (r0 + 7 * c, r0 + 7 * s), (r0 + l * c, r0 + l * s),
              SCOLOR, 1, tag="second")

    set_render_callback(on_render)


def on_resize(sender, data):
    w, h = get_main_window_size()
    size = min(w, h)
    modify_draw_command(MAIN_WINDOW, 'bg', pmax=(w, h))
    modify_draw_command(MAIN_WINDOW, 'cir',
                        center=(w // 2, h // 2), radius=.45 * size)
    add_data("oldSize", get_data("clockSize"))
    add_data("clockSize", size)


def on_render(sender, data):
    parent = get_data("parent")
    lastUpdate = get_data("lastUpdate")
    now = datetime.now()
    se = now.second
    size = get_data("clockSize")
    if se == lastUpdate and size == get_data("oldSize"):
        return
    add_data("oldSize", size)
    mi = now.minute  # + se / 60
    ho = now.hour % 12 + mi / 60
    w, h = get_main_window_size()
    x0, y0 = w // 2, h // 2
    angle = - pi / 2 + pi * ho / 6
    c, s = cos(angle), sin(angle)
    l = size * .225
    modify_draw_command(parent, "hour",
                        p1=(x0 + 7 * c, y0 + 7 * s), p2=(x0 + l * c, y0 + l * s))

    angle = - pi / 2 + pi * mi / 30
    l = size * .4
    c, s = cos(angle), sin(angle)
    modify_draw_command(parent, "minute",
                        p1=(x0 + 7 * c, y0 + 7 * s), p2=(x0 + l * c, y0 + l * s))

    angle = - pi / 2 + pi * se / 30
    c, s = cos(angle), sin(angle)
    modify_draw_command(parent, "second",
                        p1=(x0 + 7 * c, y0 + 7 * s), p2=(x0 + l * c, y0 + l * s))
    add_data("lastUpdate", se)
    print(test.counter)


def long_process():
    while True:
        test.update()
        sleep(2)


def long_process_dispatcher():
    d = threading.Thread(name='daemon', target=long_process, daemon=True)
    d.start()


with window('Non-blocking Test'):
    add_button("Start Long Callback (with thread)", callback=long_process_dispatcher)
    add_button("Start Long Callback", callback=long_process)

if __name__ == '__main__':
    with window(MAIN_WINDOW):
        set_main_window_size(W, H)
        set_main_window_title(MAIN_WINDOW)
        set_style_window_padding(0, 0)
        size = min(W, H)
        add_simple_clock(MAIN_WINDOW, size, (W // 2, H // 2))
        set_resize_callback(on_resize)
    #set_render_callback(render_call)
    long_process_dispatcher()
    start_dearpygui(primary_window=MAIN_WINDOW)
