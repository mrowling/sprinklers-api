import falcon
from falcon_cors import CORS

from .config import CONFIG
from .sprinkler import SprinklerResource, SprinklerCollection


cors = CORS(allow_origins_list=['*'])
api = application = falcon.API(middleware=[cors.middleware])

sprinklers = SprinklerResource(SprinklerCollection(CONFIG.get("sprinklers")))
api.add_route("/sprinkler/{name}", sprinklers)
