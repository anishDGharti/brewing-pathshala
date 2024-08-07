import logging
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from user_auths.models import User


logger = logging.getLogger("Django")


class CustomAuthentication(TokenAuthentication):

    def authenticate(self, request):

        token = request.META["HTTP_AUTHORIZATION"]

        if not token:
            logging.error("Token is not provided by the user")
            raise AuthenticationFailed(
                "The token needed to authenticate is not provided"
            )

        # token comes in this format <Token access_token>
        token_parts = token.split()

        if len(token_parts) != 2 or token_parts[0].lower() != "token":
            logger.error("The token provided is in invalid format.")
            raise AuthenticationFailed("The token provided is in invalid format.")
        access_token = token_parts[1]

        # authenticate user using access token
        user = self.authenticate_user(access_token)
        return (user, None)

        # authenticate user using accesstoken

    def authenticate_user(self, access_token):
        try:
            user = User.objects.get(access_token=access_token, is_active=True)
            
            return user
        except User.DoesNotExist:
            logger.error("No such user.")
            raise AuthenticationFailed("No such user.")