import json
import falcon
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

class Sprinklers(object):
    def __init__(self, config):
        self.items = {}
        for c in config:
            channel = c.get("channel")
            short_name = c.get("short_name")
            self.items[short_name] = Sprinkler(channel)

    def _find_by_name(self, name):
        return self.items.get(name)

    def trigger_by_name(self, name):
        return self._find_by_name(name).trigger()

class SprinklersResource(object):
    def __init__(self, sprinklers: Sprinklers):
        self.sprinklers = sprinklers
    def on_get(self, req, resp, name):
        doc = {
            "name": name,
        }
        self.sprinklers.trigger_by_name(name)
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status =  falcon.HTTP_200
