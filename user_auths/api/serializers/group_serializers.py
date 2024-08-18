
from rest_framework import serializers
from django.contrib.auth.models import Group

from usable.global_validations import validate_group_name



class GroupSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
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



class PermissionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    codename = serializers.CharField(max_length=100)
    content_type = serializers.CharField(max_length=100)

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'codename': instance.codename,
            'content_type': instance.content_type.model
        }