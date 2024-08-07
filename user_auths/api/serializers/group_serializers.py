
from rest_framework import serializers
from django.contrib.auth.models import Group

from usable.global_validations import validate_group_name



class GroupSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(source='pk',read_only=True)
    name = serializers.CharField(max_length=50,  error_messages={'required':("Group name must be set.")})

    def validate_name(self, value):
        return validate_group_name(value)
    
   
    def create(self, validated_data):
        return Group.objects.create(**validated_data)
    

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
