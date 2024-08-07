from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from usable import global_parameters
from usable.custom_exceptions import CustomAPIException
from usable.global_validations import validate_password, validate_phone_number
from user_auths.models import User

class UserSerializer(serializers.Serializer):
    referenceId = serializers.CharField(source="reference_id", read_only=True)
    firstName = serializers.CharField(source="first_name", max_length=20, required=False)
    lastName = serializers.CharField(source="last_name", max_length=20, required=False)
    userName = serializers.CharField(source="username", max_length=50, required=True, error_messages={"required": _("Username must be set")})
    email = serializers.EmailField(max_length=50, required=True, error_messages={"required": _("Email must be provided")})
    phoneNumber = serializers.CharField(source="phone_number", max_length=10, required=True, error_messages={"required": _("Phone Number must be set")})
    address = serializers.CharField(max_length=255, required=False)
    city = serializers.CharField(max_length=50, required=False)
    district = serializers.CharField(max_length=50, required=False)
    state = serializers.CharField(max_length=50, required=False)
    profilePicture = serializers.ImageField(source="profile_picture", required=False)
    gender = serializers.CharField(max_length=10, required=False)
    dateOfBirth = serializers.DateField(source="date_of_birth", required=False)
    accessToken = serializers.CharField(source="access_token", max_length=32, read_only=True)
    isStaff = serializers.BooleanField(source="is_staff", default=False, required=False)
    isStudent = serializers.BooleanField(source="is_student", default=False, required=False)
    isSuperUser = serializers.BooleanField(source="is_superuser", default=False, required=False)
    isActive = serializers.BooleanField(source="is_active", default=False, required=False)
    password = serializers.CharField(write_only=True, required=False)
    isDeleted = serializers.BooleanField(source='is_deleted', required=False)


    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], email=validated_data['email'], phone_number=validated_data['phone_number'], password=validated_data['password'])
        return user
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == 'password':
                instance.set_password(value)
            else:
                setattr(instance, key, value)
        instance.save()
        return instance


    def validate(self, data):
        if 'phone_number' in data:
            validate_phone_number(data["phone_number"], False)

        if self.instance:
            self._check_unique_fields(data, self.instance.reference_id)
    
        return data


    def _check_unique_fields(self, data, exclude_id):
        if 'phone_number' in data and User.objects.filter(phone_number=data["phone_number"]).exclude(reference_id=exclude_id).exists():
            raise CustomAPIException("Mobile Number already exists.")

        if 'username' in data and User.objects.filter(username=data["username"]).exclude(reference_id=exclude_id).exists():
            raise CustomAPIException("Username already exists.")

        if 'email' in data and User.objects.filter(email=data["email"], is_active=True).exclude(reference_id=exclude_id).exists():
            raise CustomAPIException("Email already exists.")


    
       