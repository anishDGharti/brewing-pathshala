from rest_framework.views import APIView
from django.contrib.auth.models import Group, Permission
from rest_framework.response import Response
from rest_framework import status
import logging

# from usable.global_functions import handle_serializer_validation
from usable.api_views import BaseApiView
from usable.custom_authentication import CustomAuthentication
from usable.custom_exceptions import CustomAPIException, custom_serializer_errors
from user_auths.api.serializers.group_serializers import GroupSerializer
from usable import global_parameters

logger = logging.getLogger("django")




class GroupAPIView(BaseApiView):
    serializer_class = GroupSerializer  
    model_name = 'auth_group'
    def get(self, request):
        return self.handle_serializer_data(Group, serializer_class=self.serializer_class)
    

    def post(self, request):
        validate_request_body =  self.validate_request_body(request)
        
        if validate_request_body:
            return validate_request_body
        try:
           
            serializer = GroupSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return self.handle_success("Group Added Successfully")

            return self.handle_invalid_serializer(serializer)

        
        except Exception as exe:
            return self.handle_view_exception(exe)
    
    def put(self, request, reference_id=None):
        return self.update(request, reference_id, partial=False)

    def patch(self, request, reference_id=None):
        return self.update(request, reference_id, partial=True)

    def update(self, request, reference_id=None, partial=False):
        validate_request_body = self.validate_request_body(request)
        if validate_request_body:
            return validate_request_body
        
        try:
            group = Group.objects.get(pk=reference_id)
            serializer = GroupSerializer(group, data=request.data, partial=partial)
            if serializer.is_valid():
                serializer.save()
                return self.handle_success("Group Updated Successfully")

            return self.handle_invalid_serializer(serializer)


        except Exception as exe:
            return self.handle_view_exception(exe)

        



    def delete(self, request, reference_id):
        try:
            group = Group.objects.get(pk=reference_id)
            group.delete()

            return self.handle_success("Group deleted succedssfully")
        except Exception as exe:
            return self.handle_view_exception(exe)


