import re

from usable.custom_exceptions import CustomAPIException




def validate_phone_number(mobile_number:str, is_null:bool, /)->str:
    """
    Validate a mobile number based on specified criteria.
    - mobile_number (str): The mobile number to validate.
    - is_null (bool): Indicates whether a null or empty string should be considered valid.
    """
    if is_null and not mobile_number:
        return True
    else:
        if mobile_number is None or mobile_number == "":
            raise CustomAPIException("Mobile number cannot be blank.")
    
    if not mobile_number.isdigit():
        raise CustomAPIException("Mobile number must be digits only.")
    
    if len(mobile_number) != 10:
        raise CustomAPIException("Mobile number must be exactly 10 digits long.")
    
    pattern = r"^(984|985|986|974|975|976|980|981|982|970|961|962|988)\d{7}$"
    if not re.match(pattern, mobile_number):
        raise CustomAPIException("Invalid mobile number pattern.")

    return True





def validate_password(password, /):
    # pattern = r"^(?=.*[A-Z])(?=.*[!@#$%^&*()])(?=.*\d).{8,}$"
    # return bool(re.match(pattern, password))
    return True






from django.contrib.auth.models import Group
from rest_framework.exceptions import ValidationError
def validate_group_name(group_name):
    # Ensure the name contains only letters and spaces
    if not re.match(r'^[A-Za-z\s]+$', group_name):
        raise ValidationError("Group name must contain only letters and spaces.")
    
    # Replace spaces with underscores
    group_name = re.sub(r'\s+', '_', group_name)
    
    # Check if the group name already exists
    if Group.objects.filter(name=group_name).exists():
        raise ValidationError(f"Group {group_name} already exists.")
    
    return group_name