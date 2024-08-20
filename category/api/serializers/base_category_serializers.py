from rest_framework import serializers

from usable.constants import CATEGORY
from ...models import BaseCategory



class BaseCategorySerializer(serializers.Serializer):
    referenceId = serializers.CharField(source="reference_id", read_only=True)
    parentCategory = serializers.ChoiceField(choices=CATEGORY, source='parent_category', error_messages={'required': 'Parent Category cannot be blank'})
    categoryName = serializers.CharField(max_length=50, source='category_name',error_messages={'required': 'Category cannot be blank'})



    def create(self, validated_data):
        return BaseCategory.objects.create(**validated_data)
    


    def update(self, instance, validated_data):
        for key, value in validated_data.items():
           
            setattr(instance, key, value)
        instance.save()
        return instance
