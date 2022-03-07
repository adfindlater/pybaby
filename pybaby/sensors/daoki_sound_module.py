#!/usr/bin/python
import RPi.GPIO as GPIO
import time

class DaokiSoundSensor(object):
    def  __init__(self, channel: int=17):
        self.channel = 17
        GPIO.setup(channel, GPIO.IN)
        GPIO.add_event_detect(self.channel, GPIO.BOTH, bouncetime=100)  # let us know when the pin goes HIGH or LOW
        GPIO.add_event_callback(self.channel, self.callback)  # assign function to GPIO PIN, Run function on change
        self.event_times = [time.time()]
        self.event_values = [-1]
        self.last_poll_time = time.time()

    def callback(self, channel):
        self.event_times.append(time.time())
        self.event_values.append(GPIO.input(channel))
        time.sleep(1e-5)

    def poll(self):
        if self.event_times[-1] > self.last_poll_time:
            self.last_poll_time = time.time()
            return True
        else:
            return False


if __name__ == "__main__":
    s = DaokiSoundSensor()

    while True:
        time.sleep(1.0)
        if s.poll():
            print("sound detected")
