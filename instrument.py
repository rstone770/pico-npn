from array import array
from machine import ADC
from power_supply import ADC_REFERENCE, HI_Z_RESISTANCE, LO_Z_RESISTANCE, PowerSupply

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

def scan_current(a: Instrument, r: float) -> float:
    if not a.ps.is_connected:
        return 0.0
    
    if a.ps.is_low_z:
        return (r - a.read()) / LO_Z_RESISTANCE
    
    return (r - a.read()) / HI_Z_RESISTANCE
