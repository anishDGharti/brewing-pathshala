




from category.api.serializers.base_category_serializers import BaseCategorySerializer
from category.models import BaseCategory
from usable.api_views import BaseApiView


class BaseCategoryApiView(BaseApiView):
    """
    Handles the creation of new categories.
    """

    model_name = "coffee_base_category"
    serializer_class = BaseCategorySerializer


    def get(self, request):
        return self.handle_serializer_data(BaseCategory, serializer_class=self.serializer_class, is_active=True, is_deleted=False)

       

