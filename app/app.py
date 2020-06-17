import json
import falcon
from .config import CONFIG
from .sprinkler import Sprinkler

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

            
api = application = falcon.API()

sprinklers = SprinklersResource(Sprinklers(CONFIG))
api.add_route("/sprinklers/{name}", sprinklers)           
