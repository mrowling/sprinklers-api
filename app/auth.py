import json
import falcon
from jose import jwt
from six.moves.urllib.request import urlopen

from .config import CONFIG

auth_config = CONFIG.get('auth')

AUTH0_DOMAIN = auth_config.get('auth0_domain')
API_AUDIENCE = auth_config.get('api_audience')
ALGORITHMS = auth_config.get('algorithms')


def get_token_auth_header(request):
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("AUTHORIZATION", None)
    if not auth:
        raise falcon.HTTPUnauthorized("Authorization header is expected")

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise falcon.HTTPUnauthorized(
            "Authorization header must start with Bearer")

    if len(parts) == 1:
        raise falcon.HTTPUnauthorized("Token not found")

    if len(parts) > 2:
        raise falcon.HTTPUnauthorized(
            "Authorization header must be Bearer token")

    token = parts[1]
    return token


def requires_auth(req):
    """Determines if the Access Token is valid
    """
    token = get_token_auth_header(req)

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
            raise falcon.HTTPUnauthorized(
                "incorrect claims please check the audience and issuer")
        except Exception:
            raise falcon.HTTPUnauthorized(
                "Unable to parse authentication token")

    return payload


class AuthMiddleware():  # pylint: disable=too-few-public-methods
    def process_resource(self, req, resp, resource, params):  # noqa # pylint: disable=unused-argument disable=no-self-use
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
        if req.method != 'OPTIONS':
            payload = requires_auth(req)
            req.context['user'] = payload


auth_middleware = AuthMiddleware()
