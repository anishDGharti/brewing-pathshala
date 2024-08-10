import logging
from decimal import Decimal

from django.db import transaction
    
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from usable import global_parameters
from usable.custom_authentication import CustomAuthentication
from usable.custom_exceptions import CustomAPIException, custom_serializer_errors

logger = logging.getLogger("django")