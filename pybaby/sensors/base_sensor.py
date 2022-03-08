class BaseSensor:
    def __init__(self, channel: int, sensor, method):
        self.channel = channel
        self.sensor = sensor
        self.method = method

    def cleanup(self, raw_output):
        return raw_output

    def poll(self):
        return self.cleanup(getattr(self.sensor, self.method)())
        
