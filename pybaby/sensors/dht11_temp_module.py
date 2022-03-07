from collections import namedtuple
import RPi.GPIO as GPIO
import dht11
import time
import datetime

humidity = namedtuple('Humidity', 'T H')

class BaseSensor:
class DHT11HumiditySensor:

    def __init__(self, channel: int = 14):
        self.channel = channel
        self.sensor = dht11.DHT11(pin=channel)
        self.temperature = None
        self.humidity = None

    def poll()
        result = instance.read()
        if result.is_valid():
            self.temperature = result.temperature
            self.humidity = humidity
            return humidity(result.temperature, result.humidity)
        else:
            return humidity(self.temperature, self.humidity)
