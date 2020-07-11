import json
import falcon
from time import sleep
from threading import Thread

from .relay import Relay
from .input import Input
from .pump import Pump


class Power(Input):
    def __init__(self, input_channel, output: Relay):
        self.output = output
        super().__init__(input_channel)

    def on(self):
        return self.output.on()

    def off(self):
        return self.output.off()

    def _pulse(self, duration):
        self.output.on()
        sleep(duration)
        self.output.off()

    def pulse(self, duration=1):
        thread = Thread(
            target=self._pulse,
            args=(duration,)
        )
        thread.start()


class PowerResource():  # pylint: disable=too-few-public-methods
    def __init__(self, power: Power, pump: Pump):
        self.power = power
        self.pump = pump

    def on_get(self, req, resp):  # pylint: disable=unused-argument
        doc = {
            "active": bool(self.power.state)
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp):  # pylint: disable=unused-argument
        try:
            self.power.pulse()
            if not req.media.get("active"):
                self.pump.clear_running()
            doc = {
                "success": True,
                "active": bool(self.power.state)
            }
            resp.body = json.dumps(doc, ensure_ascii=False)
            resp.status = falcon.HTTP_200
        except Exception as error:  # pylint: disable=broad-except
            doc = {
                "success": False,
                "message": str(error),
                "active": bool(self.power.state)
            }
            resp.body = json.dumps(doc, ensure_ascii=False)
            resp.status = falcon.HTTP_200
