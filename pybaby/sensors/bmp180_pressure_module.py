from pybaby.sensors.base_sensor import BaseSensor
from sensor import BMP180
from collections import namedtuple

altitude_tuple = namedtuple("Elevation", "m ft")

class BMP180PressureSensor(BaseSensor):
    
    def __init__(self, channel: int = 14, msl: float = 1019.303):
        BaseSensor.__init__(self, channel, BMP180(1, 0x77), "all" )
        self.msl= msl

    def cleanup(self, raw_output):
        self.pressure, self.temperature = raw_output
        self.elevation = self.pressure.altitude(self.msl)
        return self.pressure, self.temperature, self.elevation
