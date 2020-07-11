import json
import sys
from time import sleep
from multiprocessing import Process, Value
from threading import Thread, Lock

import falcon
import traceback

from .relay import Relay
from .pump import Pump


class Sprinkler():
    def __init__(self, device, channel):
        self.relay = Relay(device, channel)
        self._triggering = False
        self._sleep_duration = 1

    def _trigger(self):
        try:
            self._triggering = True
            self.relay.on()
            sleep(self._sleep_duration)
            self.relay.off()
        finally:
            self._triggering = False
            sys.stdout.flush()

    def trigger(self):
        if not self._triggering:
            thread = Thread(
                target=self._trigger,
            )
            thread.start()
        else:
            raise Exception("Already triggering")


class SprinklerCollection():
    def __init__(self, config, pump: Pump):
        self.pump = pump
        self.items = {}
        for _config in config:
            channel = _config.get("channel")
            device = _config.get("device")
            short_name = _config.get("short_name")
            self.items[short_name] = Sprinkler(device, channel)

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
