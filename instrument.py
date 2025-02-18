from array import array
from machine import ADC
from power_supply import ADC_REFERENCE, PowerSupply

class Instrument:
    SAMPLE_COUNT = 10

    id: int
    ps: PowerSupply
    probe: ADC

    def __init__(self, id: int, ps: PowerSupply, probe: ADC):
        self.id = id
        self.ps = ps
        self.probe = probe

    def read(self) -> float:
      samples = array('H', [0] * Instrument.SAMPLE_COUNT)
      mid = Instrument.SAMPLE_COUNT // 2

      for i in range(len(samples)):
        samples[i] = self.probe.read_u16()

      return (samples[mid] / 65535) * ADC_REFERENCE
      
    def disconnect(self):
        self.ps.disconnect()

    def __repr__(self) -> str:
        return f"{self.id}"
    
  
def scan_voltage(a: Instrument, b: Instrument):
    a.ps.disconnect()
    b.ps.disconnect()

    a.ps.source()
    b.ps.sink()
    v = a.read() - b.read()

    a.ps.disconnect()
    b.ps.disconnect()

    return v

def scan_diode(a: Instrument, b: Instrument):
    a_to_b = scan_voltage(a, b)
    b_to_a = scan_voltage(b, a)

    if a_to_b > 0.5 and a_to_b < 3.0 and b_to_a > 3.0:
        return (a, b, a_to_b)
    
    if b_to_a > 0.5 and b_to_a < 3.0 and a_to_b > 3.0:
        return (b, a, b_to_a)
    
    return None
