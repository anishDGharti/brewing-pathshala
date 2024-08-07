import logging
import base64


from django.contrib.auth.hashers import check_password

from user_auths.models import User



logger = logging.getLogger('django')

def login_validation(request):
    try:
        auth_header = request.META['HTTP_AUTHORIZATION']
        
        encoded_credentials = auth_header.split(' ')[1]

        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')

        email = decoded_credentials[0]
        password = decoded_credentials[1]

        try:
          
            return email, password

        except User.DoesNotExist:
            raise Exception("No such User")

    except Exception as e:
        raise Exception("No such User")


