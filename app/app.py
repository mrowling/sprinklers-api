import falcon
from .config import CONFIG
from .sprinkler import SprinklerResource, SprinklerCollection


api = application = falcon.API()

sprinklers = SprinklerResource(SprinklerCollection(CONFIG))
api.add_route("/sprinkler/{name}", sprinklers)
