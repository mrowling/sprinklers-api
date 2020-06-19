from falcon_auth import FalconAuthMiddleware, JWTAuthBackend

from .config import CONFIG

secret_key = CONFIG.get('auth').get('secret_key')

user_loader = lambda payload: payload
auth_backend = JWTAuthBackend(user_loader, secret_key=secret_key, auth_header_prefix="Bearer")
auth_middleware = FalconAuthMiddleware(auth_backend)
