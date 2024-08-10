"""
This module provides API views for managing menu items within the application.
Classes:
- MenuListApiView: Retrieves a list of menu items.
- MenuCreateApiView: Creates a new menu item.
- MenuUpdateApiView: Updates an existing menu item.
- MenuFindByIdApiView: Retrieves details of a specific menu item by ID.
- MenuDeleteApiView: Soft-deletes a menu item by marking it as deleted.
"""



import logging
from datetime import datetime

from usable.api_views import BaseApiView
from user_auths.api.serializers.menu_serializers import MenuSerializer
from user_auths.models import Menu


logger = logging.getLogger("django")



class MenuManagementApiView(BaseApiView):
    """
    API endpoint for retrieving a list of menu items.
    Retrieves a list of all active menu items.
    """
    def get(self, request):
        try:
            return self.handle_serializer_data(Menu, MenuSerializer, True, is_deleted=False)
        except Exception as exe:
            return self.handle_view_exception(exe)
        

    def post(self, request):
        validation_response = self.validate_request_body(request)
        if validation_response:
                return validation_response

        try:
            print(request.data)
            serializer = MenuSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(created_by=request.user)
                return self.handle_success("Menu created successfully.")

            return self.handle_invalid_serializer(serializer)

        except Exception as exe:
            return self.handle_view_exception(exe)
 
