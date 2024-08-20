




from category.api.serializers.base_category_serializers import BaseCategorySerializer
from category.models import BaseCategory
from usable.api_views import BaseApiView
from usable.custom_exceptions import CustomAPIException


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
                return self.handle_success(f"Category for parent category {request.data['parentCategory']}  created successfully.")

            return self.handle_invalid_serializer(serializer)
        

        except CustomAPIException as exe:
            return self.handle_custom_exception(exe)



        except Exception as exe:
            return self.handle_view_exception(exe)
 



    def put(self, request, base_category_slug):
        return self.update(request, base_category_slug, partial=False)
    

    def patch(self, request, base_category_slug):
        return self.update(request, base_category_slug, partial=True)
    


    def update(self, request, base_category_slug, partial=False):
        validate_request_body = self.validate_request_body(request)
        if validate_request_body:
            return validate_request_body
        
        try:
            base_category = BaseCategory.objects.get(category_slug=base_category_slug, is_deleted=False)
            serializer = BaseCategorySerializer(base_category, data=request.data, partial=partial,  context={'user': request.user})
            if serializer.is_valid():
                serializer.save()
                return self.handle_success("Base Category Updated Successfully")
            

            return self.handle_invalid_serializer(serializer)
        
        except CustomAPIException as exe:
            return self.handle_custom_exception(exe)



        except Exception as exe:
            return self.handle_view_exception(exe)




    def delete(self, request, base_category_slug):
        try:
            base_category = BaseCategory.objects.get(category_slug=base_category_slug, is_deleted=False)
            base_category.delete()
            return self.handle_success("Base Category deleted succedssfully")
        except Exception as exe:
            return self.handle_view_exception(exe)
