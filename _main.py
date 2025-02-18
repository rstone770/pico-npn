from math import pi, sin, cos
from diode import scan_diode
import time
from machine import ADC, I2C, Pin
from gfx import draw_diode, draw_npn, draw_pnp
from lib.ssd1306 import SSD1306_I2C
from instrument import Instrument, scan_current
from power_supply import ADC_REFERENCE, PowerSupply
from array import array

DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64

display_i2c = I2C(1, sda = Pin(6), scl = Pin(7), freq = 400000)
display = SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, display_i2c, addr = 0x3C)

probe_a = Instrument(
    1,
    ps=PowerSupply(lo_z=Pin(1), hi_z=Pin(2)),
    probe=ADC(Pin(28))
)

probe_b = Instrument(
    2,
    ps=PowerSupply(lo_z=Pin(4), hi_z=Pin(3)),
    probe=ADC(Pin(27))
)

probe_c = Instrument(
    3,
    ps=PowerSupply(lo_z=Pin(0), hi_z=Pin(29)),
    probe=ADC(Pin(26))
)

def display_diode_info(a: Instrument, b: Instrument, vfd: float):
    polarity = 1 if a.id < b.id else -1
    cathode = b.id if polarity < 0 else a.id
    anode = a.id if polarity < 0 else b.id

    display.fill(0)
    draw_diode(display, 20, 10, polarity, cathode, anode)
    display.text(f"Vfd = {vfd:.2f}V", 20, 45, 1)
    display.show()

def scan_npn_hfe(base: Instrument, collector: Instrument, emitter: Instrument):
    base.ps.disconnect()
    collector.ps.disconnect()
    emitter.ps.disconnect()

    base.ps.connect(PowerSupply.SOURCE, PowerSupply.HIGH_Z)
    collector.ps.connect(PowerSupply.SOURCE, PowerSupply.LOW_Z)
    emitter.ps.connect(PowerSupply.SINK, PowerSupply.LOW_Z)

    base_v = scan_current(base, ADC_REFERENCE)
    collector_v = scan_current(collector, ADC_REFERENCE)
    gain = collector_v / base_v

    base.ps.disconnect()
    collector.ps.disconnect()
    emitter.ps.disconnect()

    return gain

def display_npn_info(base: Instrument, collector: Instrument, emitter: Instrument, hfe: float):
    display.fill(0)
    draw_npn(display, 0, 0, collector.id, base.id, emitter.id)
    draw_pnp(display, 60, 0, collector.id, base.id, emitter.id)
    # display.text(f"Hfe = {hfe:.2f}", 20, 45, 1)
    display.show()

scans = [
    scan_diode(probe_a, probe_b),
    scan_diode(probe_a, probe_c),
    scan_diode(probe_b, probe_c)
]

diodes = [diode for diode in scans if diode is not None]
display.fill(0)

if len(diodes) == 1:
    display_diode_info(diodes[0][0], diodes[0][1], diodes[0][2])
elif len(diodes) == 2:
    left, right = diodes

    if left[0] == right[0] and left[1] != right[1]:
        hfe_lr = scan_npn_hfe(left[0], left[1], right[1])
        hfe_rl = scan_npn_hfe(left[0], right[1], left[1])

        if hfe_lr > hfe_rl:
            display_npn_info(left[0], left[1], right[1], hfe_lr)
        else:
            display_npn_info(left[0], right[1], left[1], hfe_rl)
    elif left[0] != right[0] and left[1] == right[1]:
        display.text(f"PNP {left[0]} is connected to {right[1]}", 0, 0, 1)

display.show()
