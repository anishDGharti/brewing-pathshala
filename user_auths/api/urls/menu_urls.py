from django.urls import path
from user_auths.api.views import menu_management_views

urlpatterns = [
    path("menus/",menu_management_views.MenuManagementApiView.as_view(), name='menus'),
]