from smbus2 import SMBus
from .gpio import gpio

ON = 255
OFF = 0
DEVICE_BUS = 1
bus = SMBus(DEVICE_BUS)


class Relay():
    def __init__(self, device, channel):
        self.device = device
        self.channel = channel

    def on(self):
        self._set_state(ON)

    def off(self):
        self._set_state(OFF)

    def _set_state(self, state):
        bus.write_byte_data(self.device, self.channel, state)
