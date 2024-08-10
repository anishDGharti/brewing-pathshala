from  usable.global_imports import *
from usable.handle_response import HandleResponseMixin
from usable.permission import DynamicPermissionMixin

import re
from django.utils.text import camel_case_to_spaces

class DynamicPermissionsMixin:
    model_name = None  # This should be set in subclasses

    def get_permissions(self):
        """
        Dynamically set required permissions based on the request method and model name.
        """
        if self.model_name is None:
            raise ValueError("model_name must be set in the subclass")

        # Convert the model name from CamelCase to snake_case
        snake_case_model_name = camel_case_to_spaces(self.model_name).replace(' ', '_').lower()

        # Construct permission strings based on the model name and request method
        if self.request.method == "GET":
            self.required_permissions = [f"view_{snake_case_model_name}"]
        elif self.request.method == "POST":
            self.required_permissions = [f"add_{snake_case_model_name}"]
        elif self.request.method == "PUT" or self.request.method == "PATCH":
            self.required_permissions = [f"change_{snake_case_model_name}"]
        elif self.request.method == "DELETE":
            self.required_permissions = [f"delete_{snake_case_model_name}"]

        return super().get_permissions()  # Call the parent method to apply these permissions

class BaseApiView(DynamicPermissionMixin, APIView ,HandleResponseMixin):
    permission_classes = []
    authentication_classes = [CustomAuthentication]
    
    def get_permissions(self):
        """
        Dynamically set required permissions based on the request method and model name.
        """
        if self.model_name is None:
            raise ValueError("model_name must be set in the subclass")

        # Convert the model name from CamelCase to snake_case
        snake_case_model_name = camel_case_to_spaces(self.model_name).replace(' ', '_').lower()

        # Construct permission strings based on the model name and request method
        if self.request.method == "GET":
            self.required_permissions = [f"view_{snake_case_model_name}"]
        elif self.request.method == "POST":
            self.required_permissions = [f"add_{snake_case_model_name}"]
        elif self.request.method == "PUT" or self.request.method == "PATCH":
            self.required_permissions = [f"change_{snake_case_model_name}"]
        elif self.request.method == "DELETE":
            self.required_permissions = [f"delete_{snake_case_model_name}"]

        return super().get_permissions()  # Call the parent method to apply these permissions
    
    def validate_request_body(self, request):
        """
        Validate that the request body is not empty.
        """

        if not request.body:
            return Response(
                global_parameters.BODY_NOT_BLANK_JSON, status=status.HTTP_400_BAD_REQUEST
            )
        return None
