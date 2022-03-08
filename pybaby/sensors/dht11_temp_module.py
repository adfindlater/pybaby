from pybaby.sensors.base_sensor import BaseSensor
from collections import namedtuple
import dht11

humidity_tuple = namedtuple('Humidity', 'T H')

class DHT11HumiditySensor(BaseSensor):
    
    def __init__(self, channel: int = 14):
        BaseSensor.__init__(self, channel, dht11.DHT11(pin=channel), "read")
        
    def cleanup(self, raw_output):
        if raw_output.is_valid():
            self.temperature = raw_output.temperature
            self.humidity = raw_output.humidity
            return humidity_tuple(self.temperature, self.humidity)
        else:
            return humidity_tuple(self.temperature, self.humidity)
