from lib.ssd1306 import SSD1306
from array import array

def hline(display: SSD1306, x: int, y: int, width: int, color: int = 1, weight: int = 1):
  display.fill_rect(x, y - weight // 2, width, weight, color)

def vline(display: SSD1306, x: int, y: int, height: int, color: int = 1, weight: int = 1):
  display.fill_rect(x - weight // 2, y, weight, height, color)

def draw_diode(display: SSD1306, x: int, y: int, polarity: int, cathode: int, anode: int):
    hline(display, x + 12, y + 10, 60, weight=3)
    
    if polarity <= 0:
        vline(display, x + 30, y, 20, weight=3)
        display.poly(x + 30, y + 10, array('h', [0, 0, 20, -10, 20, 10]), 1, 1)
        display.text(f"{cathode}", x, y + 7)
        display.text(f"{anode}", x + 76, y + 7)
    else:
        vline(display, x + 50, y, 20, weight=3)
        display.poly(x + 30, y + 10, array('h', [0, -10, 0, 10, 20, 0]), 1, 1)
        display.text(f"{cathode}", x, y + 7)
        display.text(f"{anode}", x + 76, y + 7)
