import falcon
import json
from jose import jwt
from six.moves.urllib.request import urlopen
from functools import wraps


from .config import CONFIG

auth = CONFIG.get('auth')

AUTH0_DOMAIN = auth.get('auth0_domain')
API_AUDIENCE = auth.get('api_audience')
ALGORITHMS = auth.get('algorithms')

class AuthMiddleware(object):
    def process_resource(self, req, resp, resource, params):
        """Process the request after routing.

        Note:
            This method is only called when the request matches
            a route to a resource.

        Args:
            req: Request object that will be passed to the
                routed responder.
            resp: Response object that will be passed to the
                responder.
            resource: Resource object to which the request was
                routed.
            params: A dict-like object representing any additional
                params derived from the route's URI template fields,
                that will be passed to the resource's responder
                method as keyword arguments.
        """
        # req.context['user'] = "MITCH"
        if req.method != 'OPTIONS':
            payload = self._requires_auth(req)
            req.context['user'] = payload

    def _requires_auth(self, req):
        """Determines if the Access Token is valid
        """
        token = self._get_token_auth_header(req)

        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)

        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise falcon.HTTPUnauthorized("token is expired")
            except jwt.JWTClaimsError:
                raise falcon.HTTPUnauthorized("incorrect claims please check the audience and issuer")
            except Exception:
                raise falcon.HTTPUnauthorized("Unable to parse authentication token")

        return payload

    def _get_token_auth_header(self, request):
        """Obtains the Access Token from the Authorization Header
        """
        auth = request.headers.get("AUTHORIZATION", None)
        if not auth:
            raise falcon.HTTPUnauthorized("Authorization header is expected")

        parts = auth.split()

        if parts[0].lower() != "bearer":
            raise AuthError({
                            "code": "invalid_header",
                            "description": "Authorization header must start with"
                            " Bearer"
                            }, 401)
        if len(parts) == 1:
            raise AuthError({"code": "invalid_header",
                            "description": "Token not found"}, 401)
        if len(parts) > 2:
            raise AuthError({"code": "invalid_header",
                            "description": "Authorization header must be Bearer token"
                            }, 401)

        token = parts[1]
        return token

auth_middleware = AuthMiddleware()
