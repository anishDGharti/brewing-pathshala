import logging
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from user_auths.models import User


logger = logging.getLogger("Django")


class CustomAuthentication(TokenAuthentication):

    def authenticate(self, request):
        # Use .get() to safely retrieve the HTTP_AUTHORIZATION header
        token = request.META.get("HTTP_AUTHORIZATION")

        if not token:
            # Return None if the header is missing, allowing access to non-authenticated views
            logger.error("Token is not provided by the user")
            return None

        # Token should come in the format "Token <access_token>"
        token_parts = token.split()

        if len(token_parts) != 2 or token_parts[0].lower() != "token":
            logger.error("The token provided is in an invalid format.")
            raise AuthenticationFailed("The token provided is in an invalid format.")
        
        access_token = token_parts[1]

        # Authenticate user using access token
        user = self.authenticate_user(access_token)
        return (user, None)

    def authenticate_user(self, access_token):
        try:
            user = User.objects.get(access_token=access_token, is_active=True)
            return user
        except User.DoesNotExist:
            logger.error("No such user.")
            raise AuthenticationFailed("No such user.")