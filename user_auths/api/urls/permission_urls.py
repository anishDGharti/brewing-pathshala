from django.urls import path

from user_auths.api.views import permission_management_views

urlpatterns = [

    # permissions
    path('permissions/group/<int:group_id>/', permission_management_views.PermissionsForGroupAndUserAPIView.as_view(), name='group-permissions'),
    path('permissions/user/<str:user_reference_id>/', permission_management_views.PermissionsForGroupAndUserAPIView.as_view(), name='user-permissions'),
]