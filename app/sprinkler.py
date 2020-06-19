from multiprocessing import Process, Value

from time import sleep
from .relay import Relay

class Sprinkler(object):
    def __init__(self, channel):
        self.relay = Relay(channel)
        self._triggering = False
        self._sleep_duration = 1
    
    @property
    def _triggering(self):
        with self._triggering_value.get_lock():
            return bool(self._triggering_value.value)
    
    @_triggering.setter
    def _triggering(self, val):
        try:
            with self._triggering_value.get_lock():
                self._triggering_value.value = val
        except AttributeError:
            self._triggering_value = Value("i", val)


    def _trigger(self):
        try:
            self._triggering = True
            self.relay.on()
            sleep(self._sleep_duration)
            self.relay.off()
        finally:
            self._triggering = False
    
    def trigger(self):
        if not self._triggering:
            process = Process(
                target=self._trigger,
                daemon=True
            )
            process.start()
        else:
            raise Exception("Already triggering")
    
    @property
    def running(self):
        return self.relay.state