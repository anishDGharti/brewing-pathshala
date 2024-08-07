import logging
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.response import Response

from rest_framework import status
from usable import global_parameters, login_auth
from usable.global_functions import uuid_generate
from user_auths.models import User

logger = logging.getLogger('django')


class LoginApiView(APIView):
    '''Login if usernme and password match it return user object of the already register user.'''
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            User
            email, password = login_auth.login_validation(request)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                token = uuid_generate()
                user.access_token= token
                user.save()
                message = {
                    "username": user.username,
                    "email": user.email,
                    "phoneNumber": user.phone_number,
                    "token":user.access_token,
                }
                return JsonResponse(message, status=status.HTTP_200_OK, safe=False)
            else:
                message = {
                    global_parameters.RESPONSE_CODE: global_parameters.UNSUCCESS_CODE,
                    global_parameters.RESPONSE_MESSAGE: global_parameters.NO_USER
                }
                return JsonResponse(message, status=status.HTTP_401_UNAUTHORIZED)
       
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            message = {
                    global_parameters.RESPONSE_CODE: global_parameters.UNSUCCESS_CODE,
                    global_parameters.RESPONSE_MESSAGE: global_parameters.NO_USER
                }
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)
        