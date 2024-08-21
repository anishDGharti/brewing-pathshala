import logging

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from usable import global_parameters
from usable.custom_exceptions import custom_serializer_errors
from usable.custom_authentication import CustomAuthentication
from usable.permission import DynamicPermissionMixin

logger = logging.getLogger("django")

class HandleResponseMixin:
    """
    Mixin to handle various API responses and exceptions.
    """
    
    @staticmethod
    def handle_success(success_message, data=None):
        """
        Handle successful responses, optionally including data.
        data (optional): The data to include in the response if available.
        """
        if data is not None:
            message = global_parameters.SUCCESS_JSON | {global_parameters.DATA: data}
        else:
            message = {
                global_parameters.RESPONSE_CODE: global_parameters.SUCCESS_CODE,
                global_parameters.RESPONSE_MESSAGE: success_message
            }
        return Response(message, status=status.HTTP_200_OK)

    @staticmethod
    def handle_serializer_data(model, serializer_class, many=True, **query):
        """
        Handle responses with serialized data from a queryset or a single instance.
        Args:
            model (Model): The Django model to query.
            serializer_class (Serializer): The serializer class to use.
            many (bool, optional): Whether to handle multiple objects (default is True).
            **query: Additional query parameters for filtering the queryset.
        """
        try:
            if many:
                model_instance = model.objects.filter(**query)
                serialized_data = serializer_class(model_instance, many=True).data
            else:
                model_instance = model.objects.get(**query)
                serialized_data = serializer_class(model_instance).data

            message = global_parameters.SUCCESS_JSON | {global_parameters.DATA: serialized_data}
            return Response(message, status=status.HTTP_200_OK)
        
        except Exception as exe:
            print(exe)
            return HandleResponseMixin.handle_view_exception(exe)
    
    @staticmethod
    def api_handle_exception():
        """
        Handle general API exceptions and return a server error response.
        """
        return Response(
            global_parameters.INTERNAL_SERVER_ERROR_JSON,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @staticmethod
    def handle_invalid_serializer(serializer):
        """
        Handle responses with serializer errors and log the errors.
        """
        # logger.error(str(serializer.errors), exc_info=True,)

        message = global_parameters.UNSUCCESS_JSON | {
            global_parameters.ERROR_DETAILS: custom_serializer_errors(serializer.errors)
        }
        print(serializer.errors)
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def handle_custom_exception(exe):
        """
        Handle custom API exceptions and log the details.
        """
        logger.error(str(exe), exc_info=True)
        message = {
            global_parameters.RESPONSE_CODE: global_parameters.UNSUCCESS_CODE,
            global_parameters.RESPONSE_MESSAGE: exe.detail,
        }
        return Response(message, status=exe.status_code)

    @staticmethod
    def handle_does_not_exist(exe):
        """
        Handle the case where a model entry does not exist and return a not found response.
        """
        message = {
            global_parameters.RESPONSE_CODE: global_parameters.UNSUCCESS_CODE,
            global_parameters.RESPONSE_MESSAGE: f"{exe}",
        }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


    def handle_view_exception(self, exe):
        """
        Determine the type of exception and delegate to the appropriate handler.
        """
        logger.error(str(exe), exc_info=True)
        if isinstance(exe, ObjectDoesNotExist):
            return self.handle_does_not_exist(exe)
        return self.api_handle_exception()



    # def handle_validation


