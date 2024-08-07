from rest_framework.exceptions import APIException

class CustomAPIException(APIException):
    def __init__(self, detail, status_code=None):
        self.detail = detail
        self.status_code = 400

def custom_serializer_errors(errors_msg):
    try:

        return [error_message for error_message_list in errors_msg.values() for error_message in error_message_list]
    except Exception as exe:
        raise Exception(exe)
