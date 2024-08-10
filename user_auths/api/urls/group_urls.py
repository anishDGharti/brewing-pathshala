from django.urls import path

from ..views import group_management_views
# from .import permission_views
urlpatterns = [
   
    # groups
    path("groups/", group_management_views.GroupAPIView.as_view(), name="groups"),
  
]