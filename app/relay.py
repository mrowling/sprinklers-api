from time import sleep
import sys
from threading import Thread
from smbus2 import SMBus

ON = 255
OFF = 0
DEVICE_BUS = 1
bus = SMBus(DEVICE_BUS)


class Relay():
    def __init__(self, device, channel, lock=None):
        self.device = device
        self.channel = channel
        self._lock = lock

    def on(self):
        self._set_state(ON)

    def off(self):
        self._set_state(OFF)

    def _set_state(self, state):
        bus.write_byte_data(self.device, self.channel, state)

    @property
    def lock(self):
        if self._lock is not None:
            return self._lock
        return False

    @lock.setter
    def lock(self, value):
        if self._lock is not None:
            self._lock = value

    def _pulse(self, duration):
        try:
            self.lock = True
            self.on()
            sleep(duration)
            self.off()
        finally:
            self.lock = False
            sys.stdout.flush()

    def pulse(self, duration):
        if not self.lock:
            thread = Thread(
                target=self._pulse,
                args=(duration,)
            )
            thread.start()
        else:
            raise Exception("Relay Locked")
