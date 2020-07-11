import json
import falcon

from .power import Power


class SequenceResource():  # pylint: disable=too-few-public-methods
    def __init__(self, power: Power):
        self.power = power

    def on_get(self, req, resp):  # pylint: disable=unused-argument
        try:
            self.power.pulse(11)
            doc = {
                "success": True,
            }
            resp.body = json.dumps(doc, ensure_ascii=False)
            resp.status = falcon.HTTP_200
        except Exception as error:  # pylint: disable=broad-except
            doc = {
                "success": False,
                "message": str(error),
            }
            resp.body = json.dumps(doc, ensure_ascii=False)
            resp.status = falcon.HTTP_200
