import falcon
from .config import CONFIG
from .sprinkler import SprinklersResource, Sprinklers


            
api = application = falcon.API()

sprinklers = SprinklersResource(Sprinklers(CONFIG))
api.add_route("/sprinklers/{name}", sprinklers)           
