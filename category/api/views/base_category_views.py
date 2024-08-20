




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



    def post(self, request):
        validate_request_body =  self.validate_request_body(request)
        if validate_request_body:
            return validate_request_body
        
        try:
            serializer = BaseCategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(created_by=request.user)
                return self.handle_success(f"Category for parent category {request.data['parentCategory']} ")
            
            return self.handle_invalid_serializer(serializer)

        except Exception as exe:
            return self.handle_view_exception(exe)
 


