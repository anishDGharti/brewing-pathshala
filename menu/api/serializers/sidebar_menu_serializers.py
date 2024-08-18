from django.contrib.auth.models import Group, Permission
from rest_framework import serializers

from menu.models import SideBarMenu
from usable.custom_exceptions import CustomAPIException
from usable import global_parameters

class  SideBarMenuSerializer(serializers.Serializer):
    referenceId = serializers.CharField(source="reference_id",read_only=True)
    menuName = serializers.CharField(source="menu_name", error_messages={'required': 'Menu name can not be blank.'})
    icon = serializers.CharField(read_only=True)
    url = serializers.CharField( error_messages={'required': 'URL cannot be blank.'})
    roles = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True)
    permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True)

    def create(self, validated_data):
        roles_data = validated_data.pop('roles')
        permissions_data = validated_data.pop('permissions')
        menu = SideBarMenu.objects.create(**validated_data)
        menu.roles.set(roles_data)
        menu.permissions.set(permissions_data)
        return menu

    def update(self, instance, validated_data):
        roles_data = validated_data.pop('roles', None)
        permissions_data = validated_data.pop('permissions', None)

        instance.menu_name = validated_data.get('menu_name', instance.menu_name)
        instance.url = validated_data.get('url', instance.url)
        instance.icon = validated_data.get('icon', instance.icon)
        instance.save()

        if roles_data is not None:
            instance.roles.set(roles_data)
        if permissions_data is not None:
            instance.permissions.set(permissions_data)

        return instance

    def validate(self, data):
        try:
            if self.instance:
                if SideBarMenu.objects.filter(menu_name=data["menu_name"]).exclude(reference_id=self.instance.reference_id).exists():
                    raise CustomAPIException("This Menu already exist.")
            else:
                if SideBarMenu.objects.filter(menu_name=data["menu_name"]).exists():
                    raise CustomAPIException("This Menu already exist.")
            
            return data
        
        except CustomAPIException as exe:
            raise serializers.ValidationError({global_parameters.ERROR_DETAILS:[exe.detail]})
           
        except Exception as exe:
           raise Exception(exe)