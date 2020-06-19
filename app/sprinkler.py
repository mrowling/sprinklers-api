import json
from time import sleep
from multiprocessing import Process, Value
import falcon

from .relay import Relay


class Sprinkler():
    def __init__(self, output_channel):
        self.relay = Relay(output_channel)
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


class SprinklerCollection():
    def __init__(self, config):
        self.items = {}
        for _config in config:
            output_channel = _config.get("output_channel")
            short_name = _config.get("short_name")
            self.items[short_name] = Sprinkler(output_channel)

    def find_by_name(self, name):
        return self.items.get(name)

    def trigger_by_name(self, name):
        return self.find_by_name(name).trigger()


class SprinklerResource():  # pylint: disable=too-few-public-methods
    def __init__(self, sprinklers: SprinklerCollection):
        self.sprinklers = sprinklers

    def on_get(self, req, resp, name):  # pylint: disable=unused-argument
        doc = {
            "name": name,
        }
        self.sprinklers.trigger_by_name(name)
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200
