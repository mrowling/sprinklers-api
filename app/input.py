from .gpio import gpio


class Input():  # pylint: disable=too-few-public-methods
    def __init__(self, channel):
        self.channel = channel
        gpio.setup(channel, gpio.IN)

    @property
    def state(self):
        return gpio.input(self.channel)
