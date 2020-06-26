import json
import falcon

from .relay import Relay
from .input import Input
from .pump import Pump


class Power():
    def __init__(self, _input: Input, output: Relay):
        self.output = output
        self.input = _input

    def on(self):
        return self.output.on()

    def off(self):
        return self.output.off()

    def state(self):
        return self.input.state


class PowerResource():  # pylint: disable=too-few-public-methods
    def __init__(self, power: Power, pump: Pump):
        self.power = power
        self.pump = pump
        self.is_power_active = True

    def on_get(self, req, resp):  # pylint: disable=unused-argument
        doc = {
            # "active": bool(self.power.state)
            "active": self.is_power_active
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp):  # pylint: disable=unused-argument
        try:
            if req.media.get("active"):
                self.power.on()
                self.is_power_active = True
            else:
                self.power.off()
                self.pump.clear_running()
                self.is_power_active = False
            doc = {
                "success": True,
                # "active": bool(self.power.state),
                # "active": bool(req.media.get("active"))
                "active": self.is_power_active
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
