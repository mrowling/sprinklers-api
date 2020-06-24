import json
import falcon

from .relay import Relay

class PowerResource():  # pylint: disable=too-few-public-methods
    def __init__(self, relay: Relay):
        self.relay = relay

    def on_get(self, req, resp):  # pylint: disable=unused-argument
        doc = {
            "on": bool(self.relay.state)
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp):  # pylint: disable=unused-argument
        try:
            if req.media.get("active"):
                self.relay.on()
            else:
                self.relay.off()
            doc = {
                "success": True,
                "active": bool(self.relay.state)
            }
            resp.body = json.dumps(doc, ensure_ascii=False)
            resp.status = falcon.HTTP_200
        except Exception as error:  # pylint: disable=broad-except
            doc = {
                "success": False,
                "message": str(error),
                "active": bool(self.relay.state)
            }
            resp.body = json.dumps(doc, ensure_ascii=False)
            resp.status = falcon.HTTP_200
