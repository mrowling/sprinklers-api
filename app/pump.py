import json
import falcon

from .input import Input


class PumpResource():  # pylint: disable=too-few-public-methods
    def __init__(self, pump: Input):
        self.pump = pump

    def on_get(self, req, resp):  # pylint: disable=unused-argument
        doc = {
            "running": self.pump.state
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200
