
from instrument import Instrument, scan_voltage

def scan_diode(a: Instrument, b: Instrument):
    a_to_b = scan_voltage(a, b)
    b_to_a = scan_voltage(b, a)

    if a_to_b > 0.5 and a_to_b < 3.0 and b_to_a > 3.0:
        return (a, b, a_to_b)
    
    if b_to_a > 0.5 and b_to_a < 3.0 and a_to_b > 3.0:
        return (b, a, b_to_a)
    
    return None

class Diode:
    cathode: Instrument
    anode: Instrument
    polarity: int
    forward_voltage: float

    def __init__(self, cathode: Instrument, anode: Instrument, polarity: int, forward_voltage: float):
        self.cathode = cathode
        self.anode = anode
        self.polarity = polarity
        self.forward_voltage = forward_voltage