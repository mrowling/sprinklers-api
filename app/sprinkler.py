from time import sleep
from .relay import Relay

class Sprinkler(object):
    def __init__(self, channel):
        self.relay = Relay(channel)
        self._triggering = False
        self._sleep_duration = 1000

    def _trigger(self):
        self.relay.on()
        sleep(self._sleep_duration)
        self.relay.off()
            
    
    def trigger(self):
        if not self._triggering:
            self._triggering = True
            self._trigger()
            self._triggering = False
        else:
            raise Exception("Already triggering")
    
    @property
    def running(self):
        return self.relay.state