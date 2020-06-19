import falcon
from .config import CONFIG
from .sprinkler import SprinklerResource, SprinklerCollection


api = application = falcon.API()

sprinklers = SprinklerResource(SprinklerCollection(CONFIG.get("sprinklers")))
api.add_route("/sprinkler/{name}", sprinklers)
