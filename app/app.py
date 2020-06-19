import falcon
from falcon_cors import CORS

from .config import CONFIG
from .auth import auth_middleware
from .sprinkler import SprinklerResource, SprinklerCollection


cors = CORS(allow_all_origins=True)
api = application = falcon.API(middleware=[cors.middleware, auth_middleware])

sprinklers = SprinklerResource(SprinklerCollection(CONFIG.get("sprinklers")))
api.add_route("/sprinkler/{name}", sprinklers)
