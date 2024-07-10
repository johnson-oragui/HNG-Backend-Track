from django.utils.deprecation import MiddlewareMixin
from authentication.utils import verify_token


class AuthorizationMiddleware(MiddlewareMixin):
    """
    Middleware for authorization
    """
    def process_request(self, request):
        """
        Processes requests.

        Returns:
            request.user or raisess an Excepion
        """
        try:
            auth_header = request.headers.get('Authorization')

            if auth_header:
                bearer, token = auth_header.split(' ')

                if bearer.lower() != "bearer" or not token:

                    request.user = None
                else:
                    payload = verify_token(token)

                    if not payload or not isinstance(payload, tuple):
                        request.user = None
                    else:
                        data = {
                            "email": payload[0],
                            "user_id": payload[1]
                        }
                        request.user = data  # attach user info to request
            else:
                request.user = None
        except Exception as exc:
            print(f'error occured in auth middleware: {exc}')
            request.user = None

    def process_response(self, request, response):
        """
        Proccesses response
        """
        return response
