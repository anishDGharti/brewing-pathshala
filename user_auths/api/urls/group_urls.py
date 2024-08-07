from django.urls import path

from ..views import group_management_views
# from .import permission_views
urlpatterns = [
   
    # groups
    path("groups/", group_management_views.GroupAPIView.as_view(), name="groups"),
   
    # permissions
    # path('permissions/group/<int:group_id>/', permission_views.PermissionsForGroupAndUserAPIView.as_view(), name='group-permissions'),
    # path('permissions/user/<str:user_reference_id>/', permission_views.PermissionsForGroupAndUserAPIView.as_view(), name='user-permissions'),
]