from django.urls import path
from menu.api.views import coffee_shop_menu_views

urlpatterns = [
    path("shop-menu/",coffee_shop_menu_views.CoffeeShopMenuApiView.as_view(), name='menu'),
]