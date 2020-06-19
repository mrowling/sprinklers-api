from .gpio import gpio


class Relay():
    def __init__(self, channel):
        self.channel = channel
        gpio.setup(channel, gpio.OUT)

    def on(self):
        self._set_state(True)

    def off(self):
        self._set_state(False)

    def toggle(self):
        self._set_state(not self.state)

    @property
    def state(self):
        return gpio.input(self.channel)

    def _set_state(self, state):
        gpio.output(self.channel, state)
