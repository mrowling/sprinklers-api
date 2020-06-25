import atexit
import falcon
from falcon_cors import CORS

from .config import CONFIG
from .gpio import gpio
from .auth import auth_middleware
from .sprinkler import SprinklerResource, SprinklerCollection
from .pump import PumpResource, Pump
from .relay import Relay
from .power import PowerResource


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

power = Relay(CONFIG.get("power").get("channel"))
power_resource = PowerResource(power, pump)
api.add_route("/power", power_resource)


@atexit.register
def cleanup():
    gpio.cleanup()
    print("Cleanup Complete")
