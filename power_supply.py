from machine import Pin

ADC_REFERENCE = 3.3

class PowerSupply:
    SINK = 0
    SOURCE = 1

    LOW_Z = 0
    HIGH_Z = 1

    __polarity: int | None = None
    __impedance: int | None = None

    __lo_z: Pin
    __hi_z: Pin

    def __init__(self, lo_z: Pin, hi_z: Pin):
        self.__lo_z = lo_z
        self.__lo_z.init(Pin.OPEN_DRAIN, value=1)

        self.__hi_z = hi_z
        self.__hi_z.init(Pin.OPEN_DRAIN, value=1)
    
    @property
    def is_connected(self) -> bool:
        return self.__polarity is not None

    @property
    def is_sink(self) -> bool:
        return self.__polarity == PowerSupply.SINK

    @property
    def is_source(self) -> bool:
        return self.__polarity == PowerSupply.SOURCE

    @property
    def is_low_z(self) -> bool:
        return self.__impedance == PowerSupply.LOW_Z

    @property
    def is_high_z(self) -> bool:
        return self.__impedance == PowerSupply.HIGH_Z

    def disconnect(self):
        self.__lo_z.init(Pin.OPEN_DRAIN, value=1)
        self.__hi_z.init(Pin.OPEN_DRAIN, value=1)
        self.__polarity = None
        self.__impedance = None

    def connect(self, polarity: int, impedance: int):
        if polarity not in (PowerSupply.SINK, PowerSupply.SOURCE):
            raise ValueError("Invalid polarity")
        
        if impedance not in (PowerSupply.LOW_Z, PowerSupply.HIGH_Z):
            raise ValueError("Invalid impedance")
        
        lo_z = self.__lo_z
        hi_z = self.__hi_z

        # Disconnect everything first
        lo_z.init(Pin.OPEN_DRAIN, value=1)
        hi_z.init(Pin.OPEN_DRAIN, value=1)
    
        if polarity == PowerSupply.SINK and impedance == PowerSupply.LOW_Z:
            lo_z.init(Pin.OPEN_DRAIN, value=0)
        elif polarity == PowerSupply.SINK and impedance == PowerSupply.HIGH_Z:
            hi_z.init(Pin.OPEN_DRAIN, value=0)
        elif polarity == PowerSupply.SOURCE and impedance == PowerSupply.LOW_Z:
            lo_z.init(Pin.OUT, value=1)
        elif polarity == PowerSupply.SOURCE and impedance == PowerSupply.HIGH_Z:
            hi_z.init(Pin.OUT, value=1)

        self.__polarity = polarity
        self.__impedance = impedance

    def sink(self):
        self.connect(PowerSupply.SINK, self.__impedance or PowerSupply.LOW_Z)

    def source(self):
        self.connect(PowerSupply.SOURCE, self.__impedance or PowerSupply.LOW_Z)

    def low_z(self):
        self.connect(self.__polarity or PowerSupply.SINK, PowerSupply.LOW_Z)

    def high_z(self):
        self.connect(self.__polarity or PowerSupply.SINK, PowerSupply.HIGH_Z)
