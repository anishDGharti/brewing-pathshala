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

    model_name = "coffee_user"
    serializer_class = UserSerializer
   


    def get(self, request):
        filter_query = request.query_params.get('filter_query')
        query_set = filter_user(request, filter_query)

        if query_set is None:
            message = {
                global_parameters.RESPONSE_CODE: global_parameters.SUCCESS_CODE,
                global_parameters.RESPONSE_MESSAGE: "No users found",
            }
            return Response(message, status=status.HTTP_200_OK)
        
        return self.handle_serializer_data(User, serializer_class=self.serializer_class, **query_set)

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
     
    def post(self, request):
        validate_request_body =  self.validate_request_body(request)
        if validate_request_body:
            return validate_request_body
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
                
                return self.handle_success("User Created Successfully")
 
            return self.handle_invalid_serializer(serializer)
       
        except CustomAPIException as exe:
            return self.handle_custom_exception(exe)



        except Exception as exe:
            return self.handle_view_exception(exe)

    def put(self, request, reference_id=None):
        return self.update(request, reference_id, partial=False)

    def patch(self, request, reference_id=None):
        return self.update(request, reference_id, partial=True)

    def update(self, request, reference_id=None, partial=False): 
        validate_request_body =  self.validate_request_body(request)
        if validate_request_body:
            return validate_request_body
        try:
            user = User.objects.get(reference_id=reference_id, is_deleted=False)
            serializer = UserSerializer(user, data=request.data, partial=partial, context={'user': request.user})
            if serializer.is_valid():
                serializer.save()
                return self.handle_success("User Updated Successfully")
            

            return self.handle_invalid_serializer(serializer)

        except CustomAPIException as exe:
            return self.handle_custom_exception(exe)



        except Exception as exe:
            return self.handle_view_exception(exe)
        


    def delete(self, request, reference_id):
        try:
            user = User.objects.get(reference_id=reference_id, is_deleted=False)
            user.delete()

            return self.handle_success("User deleted succedssfully")
        except Exception as exe:
            return self.handle_view_exception(exe)






