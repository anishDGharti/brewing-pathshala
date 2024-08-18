from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed, AuthenticationFailed
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from usable import global_parameters

class CustomAPIException(APIException):
    def __init__(self, detail, status_code=None):
        self.detail = detail
        self.status_code = 400

def custom_serializer_errors(errors_msg):
    try:

        return [error_message for error_message_list in errors_msg.values() for error_message in error_message_list]
    except Exception as exe:
        raise Exception(exe)





def custom_exception_handler(exc, context):
    if isinstance(exc, AuthenticationFailed):

        return Response({
            global_parameters.RESPONSE_CODE: global_parameters.UNSUCCESS_CODE,
            global_parameters.RESPONSE_MESSAGE:"Authentication credentials were not provided.!"
        },  status=status.HTTP_401_UNAUTHORIZED)
    
    if isinstance(exc, MethodNotAllowed):
        return Response({
            global_parameters.RESPONSE_CODE: global_parameters.UNSUCCESS_CODE,
            global_parameters.RESPONSE_MESSAGE:"Method Not allowed, use appropriate Method!"
        },status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    if isinstance(exc, PermissionDenied):
        response = Response(global_parameters.UNSUCCESS_JSON | {'message':'You donot have required permission to view this page.'}, status=status.HTTP_403_FORBIDDEN,
        )
        return response

    response = exception_handler(exc, context)

    return response
