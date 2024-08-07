import logging

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from user_auths.models import User

logger = logging.getLogger('django')

class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            logger.error("Token is not provided by user.")
            raise AuthenticationFailed('Authentication token not provided.')

        parts = token.split()
        if len(parts) != 2 or parts[0].lower() != 'token':
            logger.error("Invalid token format.")
            raise AuthenticationFailed('Invalid token format.')

        session_id = parts[1]
        
        user = self.authenticate_user(session_id)
        return (user, None)

    def authenticate_user(self, session_id):
        try:
            user = User.objects.get(token=session_id, is_active=True)
            return user
        except User.DoesNotExist:
            raise AuthenticationFailed('No such user.', code=401)
        except Exception:
            raise AuthenticationFailed('No such user.')

    def authenticate_header(self, request):
        """
        Return a string to be used in the `WWW-Authenticate` header.
        """
        return 'Token realm="api"'  # Customize as needed
