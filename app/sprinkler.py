import json

import falcon

from .relay import Relay
from .pump import Pump


class Sprinkler():  # pylint: disable=too-few-public-methods
    def __init__(self, device, channel, lock):
        self.relay = Relay(device, channel, lock)
        self._triggering = False

    def trigger(self, duration=1):
        self.relay.pulse(duration)


class SprinklerCollection():
    def __init__(self, config, pump: Pump):
        self.pump = pump
        self.items = {}
        self._lock = False
        for _config in config:
            channel = _config.get("channel")
            device = _config.get("device")
            short_name = _config.get("short_name")
            self.items[short_name] = Sprinkler(device, channel, self._lock)

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
