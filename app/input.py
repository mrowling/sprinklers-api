from .gpio import gpio
from .config import CONFIG

pull_up_down = CONFIG.get('gpio').get('pull_up_down')
pull_up_down = getattr(gpio, pull_up_down)


class Input():  # pylint: disable=too-few-public-methods
    def __init__(self, channel):
        self.channel = channel
        gpio.setup(channel, gpio.IN, pull_up_down=pull_up_down)

    @property
    def state(self):
        return gpio.input(self.channel)
