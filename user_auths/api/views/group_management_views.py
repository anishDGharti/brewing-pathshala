from rest_framework.views import APIView
from django.contrib.auth.models import Group, Permission
from rest_framework.response import Response
from rest_framework import status
import logging

# from usable.global_functions import handle_serializer_validation
from usable.custom_authentication import CustomAuthentication
from usable.custom_exceptions import CustomAPIException, custom_serializer_errors
from user_auths.api.serializers.group_serializers import GroupSerializer
from usable import global_parameters

logger = logging.getLogger("django")




class GroupAPIView(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = []
    serializer_class = GroupSerializer  
    def get(self, request):
      
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        message = global_parameters.SUCCESS_JSON | {global_parameters.DATA: serializer.data}
        return Response(message, status=status.HTTP_200_OK)
    

    def post(self, request):
        try:
            if not request.body:
                return Response(global_parameters.BODY_NOT_BLANK_JSON, status=status.HTTP_400_BAD_REQUEST)

            group_serializer = GroupSerializer(data=request.data)
            if group_serializer.is_valid():
                group_serializer.save()
                message = {
                    global_parameters.RESPONSE_CODE: global_parameters.SUCCESS_CODE,
                    global_parameters.RESPONSE_MESSAGE: "Group Created successfully.",
                    'message':'Group created Successfully',
                }
                return Response(message, status=status.HTTP_200_OK)

            message = global_parameters.UNSUCCESS_JSON|{global_parameters.ERROR_DETAILS:custom_serializer_errors(group_serializer.errors)}

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
            group = Group.objects.get(pk=reference_id)
            serializer = GroupSerializer(group, data=request.data, partial=partial)
            if serializer.is_valid():
                serializer.save()
                message = {
                    global_parameters.RESPONSE_CODE: global_parameters.SUCCESS_CODE,
                    global_parameters.RESPONSE_MESSAGE: "Group updated successfully."
                }
                return Response(message, status=status.HTTP_200_OK)

            message = global_parameters.UNSUCCESS_JSON | {global_parameters.ERROR_DETAILS: custom_serializer_errors(serializer.errors)}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        except Group.DoesNotExist as exe:
            logger.error(str(exe), exc_info=True)
            message = {
                global_parameters.RESPONSE_CODE: global_parameters.UNSUCCESS_CODE,
                global_parameters.RESPONSE_MESSAGE: "Group with the given reference id not found"
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response(global_parameters.INTERNAL_SERVER_ERROR_JSON, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



    def delete(self, request, reference_id):
        try:
            group = Group.objects.get(pk=reference_id)
            group.delete()

            message = {
                    global_parameters.RESPONSE_CODE: global_parameters.SUCCESS_CODE,
                    global_parameters.RESPONSE_MESSAGE: "Group deleted Successfully.",
            }
            return Response(message, status=status.HTTP_200_OK)
        
        except Group.DoesNotExist as exe:
            logger.error(str(exe), exc_info=True)
            message = {
                global_parameters.RESPONSE_CODE: global_parameters.UNSUCCESS_CODE,
                global_parameters.RESPONSE_MESSAGE:"Group data not found."
            }
            return Response(message, status = status.HTTP_400_BAD_REQUEST)
        
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            return Response(global_parameters.INTERNAL_SERVER_ERROR_JSON, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

