from django.urls import path
from user_auths.api.views import user_management_views, login_user_views

urlpatterns = [
    path("users/",user_management_views.UserManagementApiView.as_view(), name='users'),
    path("login-user/",login_user_views.LoginApiView.as_view(), name='login-user'),
    path("users/<str:reference_id>/", user_management_views.UserManagementApiView.as_view(), name='manage-user'),
]