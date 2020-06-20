import falcon
from falcon_cors import CORS

from .config import CONFIG
from .auth import auth_middleware
from .sprinkler import SprinklerResource, SprinklerCollection
from .pump import PumpResource, Pump


cors = CORS(
    allow_all_origins=True,
    allow_all_headers=True,
    allow_all_methods=True
)
middleware = [
    cors.middleware,
    auth_middleware,
]
api = application = falcon.API(middleware=middleware)

pump = Pump(CONFIG.get("pump").get("channel"))
pump_resource = PumpResource(pump)
api.add_route("/pump", pump_resource)

sprinkler = SprinklerCollection(CONFIG.get("sprinklers"), pump)
sprinkler_resource = SprinklerResource(sprinkler)
api.add_route("/sprinkler/{name}", sprinkler_resource)
