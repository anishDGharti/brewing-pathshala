from rest_framework import serializers

from usable.constants import CATEGORY
from usable.custom_exceptions import CustomAPIException
from ...models import BaseCategory



class BaseCategorySerializer(serializers.Serializer):
    referenceId = serializers.CharField(source="reference_id", read_only=True)
    parentCategory = serializers.ChoiceField(choices=CATEGORY, source='parent_category', error_messages={'required': 'Parent Category cannot be blank'})
    categoryName = serializers.CharField(max_length=50, source='category_name',error_messages={'required': 'Category cannot be blank'})


    def validate(self, data):
        if BaseCategory.objects.filter(category_name=data['category_name'], is_deleted=False, is_active=True).exists():
            raise CustomAPIException(f"Category with name '{data['category_name']}' already exists.")
        return data

    def create(self, validated_data):
        return BaseCategory.objects.create(**validated_data)
    


    def update(self, instance, validated_data):
        for key, value in validated_data.items():
           
           
            setattr(instance, key, value)
        instance.save()
        return instance
