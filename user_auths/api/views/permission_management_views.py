from django.shortcuts import get_object_or_404

import logging

from usable import global_parameters
from usable.api_views import BaseApiView
from user_auths.api.serializers.group_serializers import PermissionSerializer
from user_auths.models import User

logger = logging.getLogger("django")





from django.contrib.auth.models import Group, Permission
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.contrib.contenttypes.models import ContentType


content_types = ContentType.objects.all()
all_permissions = Permission.objects.filter(content_type__in=content_types).prefetch_related('content_type')
# cache this for optimiztion

class PermissionsForGroupAndUserAPIView(BaseApiView):

    model_name = 'permission'
    def get(self, request, user_reference_id=None, group_id=None):
        try:
            if group_id:
                group = get_object_or_404(Group, pk=group_id)
                selected_permissions = group.permissions.all()
            elif user_reference_id:
                user = get_object_or_404(User, reference_id=user_reference_id)
                selected_permissions = user.user_permissions.all()

        except Exception as exc:
            return self.handle_does_not_exist()
        
        available_permissions = set(all_permissions) - set(selected_permissions)

        # Serialize both selected and available permissions in one go.
        serialized_data = {
            'selected_permissions': PermissionSerializer(selected_permissions, many=True).data,
            'available_permissions': PermissionSerializer(available_permissions, many=True).data
        }

        message = global_parameters.SUCCESS_JSON | {global_parameters.DATA: serialized_data}
        return Response(message, status=status.HTTP_200_OK)
    

    def post(self, request, user_reference_id=None, group_id=None):
        """Updates permissions for a group or user."""
        validation_response = self.validate_request_body(request)
        if validation_response:
                return validation_response
        permission_ids = request.data.get('permissions', [])
        new_permissions = set(Permission.objects.filter(id__in=permission_ids))
        try:
            if group_id:
                group = get_object_or_404(Group, pk=group_id)
                group.permissions.set(new_permissions)
                selected_permissions = group.permissions.all()
            elif user_reference_id:
                user = get_object_or_404(User, reference_id=user_reference_id)
                user.user_permissions.set(new_permissions)
                selected_permissions = user.user_permissions.all()
        except Exception as exc:
            return self.handle_does_not_exist()
        
        # Calculate available permissions after the update
        available_permissions = set(all_permissions) - set(selected_permissions)

        serialized_data = {
            'selected_permissions': PermissionSerializer(selected_permissions, many=True).data,
            'available_permissions': PermissionSerializer(available_permissions, many=True).data
        }
        message = global_parameters.SUCCESS_JSON | {global_parameters.DATA: serialized_data}
        return Response(message, status=status.HTTP_200_OK)

        





