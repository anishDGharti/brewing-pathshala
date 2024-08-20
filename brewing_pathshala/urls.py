
from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('', include('user_auths.api.urls.auth_urls')),
    path('', include('user_auths.api.urls.group_urls')),
    path('', include('user_auths.api.urls.permission_urls')),

    path('', include('menu.api.urls.sidebar_menu_urls')),
    path('', include('menu.api.urls.coffee_shop_menu_urls')),

    path('', include('category.api.urls.base_category_urls')),



    # swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
