from lib.ssd1306 import SSD1306
from array import array

def draw_diode(display: SSD1306, x: int, y: int, polarity: int, cathode: int, anode: int):
    display.hline(x + 12, y + 10, 45, 1)
    
    if polarity <= 0:
        display.vline(x + 25, y, 20, 1)
        display.poly(x + 25, y + 10, array('h', [0, 0, 15, -10, 15, 10]), 1, 1)
        display.text(f"{cathode}", x, y + 7)
        display.text(f"{anode}", x + 62, y + 7)
    else:
        display.vline(x + 50, y, 20, 1)
        display.poly(x + 30, y + 10, array('h', [0, -10, 0, 10, 15, 0]), 1, 1)
        display.text(f"{cathode}", x, y + 7)
        display.text(f"{anode}", x + 62, y + 7)

def draw_npn(display: SSD1306, x: int, y: int, collector: int, base: int, emitter: int):
    display.ellipse(x + 30, y + 30, 15, 15, 1, 0)
    display.hline(x + 10, y + 30, 11, 1)
    display.fill_rect(x + 22, y + 20, 5, 20, 1)
    display.text(f"{base}", x, y + 26)

    # collector
    display.line(x + 26, y + 27, x + 36, y + 17, 1) 
    display.vline(x + 36, y + 10, 8, 1)
    display.text(f"{collector}", x + 32, y)
    
    # emitter
    display.line(x + 26, y + 33, x + 36, y + 43, 1) 
    display.vline(x + 36, y + 43, 8, 1)
    display.poly(x + 36, y + 42, array('h', [0, 0, -3, -5, -5, -1]), 1, 1)
    display.text(f"{emitter}", x + 32, y + 54)

def draw_pnp(display: SSD1306, x: int, y: int, collector: int, base: int, emitter: int):
    display.ellipse(x + 30, y + 30, 15, 15, 1, 0)
    display.hline(x + 10, y + 30, 11, 1)
    display.fill_rect(x + 22, y + 20, 5, 20, 1)
    display.text(f"{base}", x, y + 26)

    # collector
    display.line(x + 26, y + 27, x + 36, y + 17, 1) 
    display.vline(x + 36, y + 10, 8, 1)
    display.text(f"{collector}", x + 32, y)
    
    # emitter
    display.line(x + 26, y + 33, x + 36, y + 43, 1) 
    display.vline(x + 36, y + 43, 8, 1)
    display.poly(x + 27, y + 33, array('h', [0, 0, 3, 6, 5, 3]), 1, 1)
    display.text(f"{emitter}", x + 32, y + 54)