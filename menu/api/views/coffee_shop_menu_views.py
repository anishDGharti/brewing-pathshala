from usable.api_views import BaseApiView
from  usable.global_imports import *

from menu.api.serializers.coffee_shop_menu_serializers import CoffeeShopMenuSerializer
from menu.models import CoffeeShopMenu
from usable.custom_authentication import CustomAuthentication



class CoffeeShopMenuApiView(BaseApiView):
    serializer_class = CoffeeShopMenuSerializer
    authentication_classes = [CustomAuthentication]
    permission_classes = []
    model_name = 'coffee_shop_menu'
    



    def get(self, request):
            return self.handle_serializer_data(CoffeeShopMenu, self.serializer_class, True, is_active=True, is_deleted=False)
       