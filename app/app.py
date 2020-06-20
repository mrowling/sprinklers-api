import falcon
from falcon_cors import CORS

from .config import CONFIG
from .auth import auth_middleware
from .sprinkler import SprinklerResource, SprinklerCollection
from .pump import PumpResource
from .input import Input


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

sprinkler = SprinklerResource(SprinklerCollection(CONFIG.get("sprinklers")))
api.add_route("/sprinkler/{name}", sprinkler)

pump = PumpResource(Input(CONFIG.get("pump").get("channel")))
api.add_route("/pump", pump)
