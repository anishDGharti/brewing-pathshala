from rest_framework import serializers
from django.utils.text import slugify
from usable.constants import CATEGORY
from usable.custom_exceptions import CustomAPIException
from ...models import BaseCategory



class BaseCategorySerializer(serializers.Serializer):
    referenceId = serializers.CharField(source="reference_id", read_only=True)
    parentCategory = serializers.ChoiceField(choices=CATEGORY, source='parent_category', error_messages={'required': 'Parent Category cannot be blank'})
    categoryName = serializers.CharField(max_length=50, source='category_name',error_messages={'required': 'Category cannot be blank'})


    def validate(self, data):
        category_name = data['category_name']
        parent_category = data['parent_category']
        category_slug = slugify(category_name)

        # Check if the category name already exists within the same parent category
        if BaseCategory.objects.filter(
            category_name=category_name,
            parent_category=parent_category,
            is_active=True,
            is_deleted=False
        ).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError(f"Category name '{category_name}' already exists for this parent category.")

        # Check if the slug already exists
        base_slug = category_slug
        slug_count = BaseCategory.objects.filter(
            category_slug__startswith=base_slug,
            
        ).exclude(pk=self.instance.pk if self.instance else None).count()

        if slug_count > 0:
            # Append a number to the slug if a slug conflict is found
            category_slug = f"{base_slug}-{slug_count + 1}"

        # Save the final slug in the validated_data
        data['category_slug'] = category_slug

        return data
    
     
    def create(self, validated_data):
      
        return BaseCategory.objects.create(**validated_data)


    def update(self, instance, validated_data):
        for key, value in validated_data.items():
           
           
            setattr(instance, key, value)
       

        instance.save()
        return instance
