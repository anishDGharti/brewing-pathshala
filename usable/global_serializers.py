



from datetime import datetime

def update_current_serializer(self,instance, validated_data, request):
    for attribute, attribute_value in validated_data.items():
        instance.updated_by = request.user
        instance.updated_at =  datetime.now()
        setattr(instance, attribute, attribute_value)
