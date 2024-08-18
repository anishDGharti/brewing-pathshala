from django.db import models
from django.conf import settings
from .generators import generate_uuid

from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.
class BaseModel(models.Model):
    reference_id = models.CharField(max_length=32, unique=True, null=False, default=generate_uuid)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,db_column="created_by",related_name="+",null=True,blank=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,db_column="updated_by",related_name="+",null=True,)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False, help_text="Status to check if the user is active")

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    remarks = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        abstract = True



    unique_fields = []  

    objects = models.Manager()  
    active_objects = models.Manager()  

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self, *args, **kwargs):
        super(BaseModel, self).delete(*args, **kwargs)

    def clean(self):
        for field in self.unique_fields:
            
            if self._meta.model.objects.filter(**{field: getattr(self, field)}, is_deleted=False).exclude(id=self.id).exists():
                raise ValidationError(f'A record with this {field} already exists.')


    @classmethod
    def get_active_objects(cls):
        return cls.objects.filter(is_deleted=False, is_active=True)    

