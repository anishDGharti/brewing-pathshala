from django.shortcuts import render
import logging
from  usable.global_imports import *
from usable.global_validations import validate_password
from usable.global_filters import filter_user

from usable.api_views import BaseApiView
from user_auths.api.serializers.user_serializers import UserSerializer
from user_auths.models import User

logger = logging.getLogger('django')

class UserManagementApiView(BaseApiView):
    """
    Handles the registration of new users. This view does not require authentication or permissions.
    """

    model_name = "user"

    def _validate_creation(self, data):

        if not data.get("password"):
            raise CustomAPIException("Password cannot be blank.")
        if not validate_password(data["password"]):
            raise CustomAPIException("Password must contain at least one uppercase letter, one lowercase letter, one digit, and be at least 8 characters long.")


        existing_user = User.objects.filter(email=data.get("email")).first()
        if existing_user:
            if not existing_user.is_deleted:
                raise CustomAPIException("Email already exists.")
            else:
                data['existing_user'] = existing_user

        
        existing_user = User.objects.filter(phone_number=data.get("phoneNumber")).first()
        if existing_user:
            if not existing_user.is_deleted:
                raise CustomAPIException("Mobile Number already exists.")
            else:
                data['existing_user'] = existing_user
        


        existing_user = User.objects.filter(username=data.get("userName")).first()
        
        if existing_user:
            if not existing_user.is_deleted:
                raise CustomAPIException("Username already exists.")
            else:
                data['existing_user'] = existing_user


    def get(self, request):
        filter_query = request.query_params.get('filter_query')
        query_set = filter_user(request, filter_query)

        if query_set is None:
            message = {
                global_parameters.RESPONSE_CODE: global_parameters.SUCCESS_CODE,
                global_parameters.RESPONSE_MESSAGE: "No users found",
            }
            return Response(message, status=status.HTTP_200_OK)
        
        serializer = UserSerializer(query_set, many=True)
        message = global_parameters.SUCCESS_JSON | {global_parameters.DATA: serializer.data}
        return Response(message, status=status.HTTP_200_OK)
    
     
    def post(self, request):
        if not request.body:
                return Response(global_parameters.BODY_NOT_BLANK_JSON, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = request.data.copy()
            self._validate_creation(data)

            if 'existing_user' in data:
                user = data['existing_user']
                user.is_deleted = False
                serializer = UserSerializer(user, data=request.data, context={'request': request}, partial=True)
            else:
                serializer = UserSerializer(data=request.data, context={'request': request})

            if serializer.is_valid():

                serializer.save()
                message = {
                    global_parameters.RESPONSE_CODE: global_parameters.SUCCESS_CODE,
                    global_parameters.RESPONSE_MESSAGE: "User register successfully.",
                    'message':'User registered Successfully',
                }
                return Response(message, status=status.HTTP_200_OK)
 
            
            message = global_parameters.UNSUCCESS_JSON|{global_parameters.ERROR_DETAILS:custom_serializer_errors(serializer.errors)}

            return Response(message, status = status.HTTP_400_BAD_REQUEST)
        
        except CustomAPIException as exc:
            logger.error(str(exc), exc_info=True)
            message = {
                global_parameters.RESPONSE_CODE: global_parameters.UNSUCCESS_CODE,
                global_parameters.RESPONSE_MESSAGE: str(exc),
            }
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response(global_parameters.INTERNAL_SERVER_ERROR_JSON, status=status.HTTP_500_INTERNAL_SERVER_ERROR,)

    def put(self, request, reference_id=None):
        return self.update(request, reference_id, partial=False)

    def patch(self, request, reference_id=None):
        return self.update(request, reference_id, partial=True)

    def update(self, request, reference_id=None, partial=False): 
        if not request.body:
            return Response(global_parameters.BODY_NOT_BLANK_JSON, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(reference_id=reference_id, is_deleted=False)
            serializer = UserSerializer(user, data=request.data, partial=partial, context={'user': request.user})
            if serializer.is_valid():
                serializer.save()
                message = {
                    global_parameters.RESPONSE_CODE: global_parameters.SUCCESS_CODE,
                    global_parameters.RESPONSE_MESSAGE: "User updated successfully."
                }
                return Response(message, status=status.HTTP_200_OK)

            message = global_parameters.UNSUCCESS_JSON | {global_parameters.ERROR_DETAILS: custom_serializer_errors(serializer.errors)}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist as exe:
            logger.error(str(exe), exc_info=True)
            message = {
                global_parameters.RESPONSE_CODE: global_parameters.UNSUCCESS_CODE,
                global_parameters.RESPONSE_MESSAGE: "User with the given reference id not found"
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND)
    
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response(global_parameters.INTERNAL_SERVER_ERROR_JSON, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


    def delete(self, request, reference_id):
        try:
            user = User.objects.get(reference_id=reference_id, is_deleted=False)
            user.delete()

            message = {
                    global_parameters.RESPONSE_CODE: global_parameters.SUCCESS_CODE,
                    global_parameters.RESPONSE_MESSAGE: "User deleted Successfully.",
            }
            return Response(message, status=status.HTTP_200_OK)
        
        except User.DoesNotExist as exe:
            logger.error(str(exe), exc_info=True)
            message = {
                global_parameters.RESPONSE_CODE: global_parameters.UNSUCCESS_CODE,
                global_parameters.RESPONSE_MESSAGE:"User data not found."
            }
            return Response(message, status = status.HTTP_400_BAD_REQUEST)
        
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response(global_parameters.INTERNAL_SERVER_ERROR_JSON, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        










