import json
from time import sleep
from multiprocessing import Process, Value
import falcon

from .relay import Relay
from .pump import Pump


class Sprinkler():
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
        return bool(self.relay.state)


class SprinklerCollection():
    def __init__(self, config, pump: Pump):
        self.pump = pump
        self.items = {}
        for _config in config:
            channel = _config.get("channel")
            short_name = _config.get("short_name")
            self.items[short_name] = Sprinkler(channel)

    def find_by_name(self, name) -> Sprinkler:
        return self.items.get(name)

    def trigger_by_name(self, name):
        if not self.pump.safe_to_trigger(name):
            raise Exception("Not safe to trigger")
        self.find_by_name(name).trigger()
        self.pump.set_running(name)


class SprinklerResource():  # pylint: disable=too-few-public-methods
    def __init__(self, sprinklers: SprinklerCollection):
        self.sprinklers = sprinklers

    def on_get(self, req, resp, name):  # pylint: disable=unused-argument
        sprinkler = self.sprinklers.find_by_name(name)
        sprinkler.trigger()
        doc = {
            "name": name,
            "running": sprinkler.running
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp, name):  # pylint: disable=unused-argument
        try:
            self.sprinklers.trigger_by_name(name)
            doc = {
                "name": name,
                "success": True
            }
            resp.body = json.dumps(doc, ensure_ascii=False)
            resp.status = falcon.HTTP_200
        except Exception as error:  # pylint: disable=broad-except
            doc = {
                "name": name,
                "success": False,
                "message": str(error)
            }
            resp.body = json.dumps(doc, ensure_ascii=False)
            resp.status = falcon.HTTP_200
