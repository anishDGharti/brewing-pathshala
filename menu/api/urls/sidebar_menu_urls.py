from django.urls import path
from ..views import sidebar_menu_management_views

urlpatterns = [
    path("sidebar-menus/",sidebar_menu_management_views.SideBarMenuManagementApiView.as_view(), name='sidebar-menus'),
]