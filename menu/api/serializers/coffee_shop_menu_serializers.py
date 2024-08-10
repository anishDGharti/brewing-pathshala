from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from menu.models import CoffeeShopMenu
from usable import global_parameters
from usable.custom_exceptions import CustomAPIException
from usable.global_serializers import update_current_serializer



MENU_ITEMS = (
        ('coffee', 'Coffee'),
        ('tea', 'Tea'),
        ('bakery_item', 'Bakery Item'),
        # Add more menu items here if needed
    )



class CoffeeShopMenuSerializer(serializers.Serializer):
    referenceId = serializers.CharField(source="reference_id",read_only=True)
    menu = serializers.ChoiceField( choices=MENU_ITEMS, error_messages={'required': 'Menu Name cannot be blank'})
    menuItem = serializers.CharField(source='menu_item', error_messages={'required': 'Menu Item cannot be blank'})
    ingredientsAdded = serializers.CharField(source='ingredients_added', error_messages={'required': 'Menu Item cannot be blank'})
    price = serializers.DecimalField( max_digits=10, decimal_places=2,error_messages={'required': 'Price mist be set'})
   


    def create(self, validated_data):
        return CoffeeShopMenu.objects.create(**validated_data)
    

    def update(self, instance, validated_data):
        update_current_serializer(self, instance, validated_data)