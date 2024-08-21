from django.db import models

from usable.base_models import BaseModel
from usable.constants import CATEGORY
# Create your models here.
from django.core.exceptions import ValidationError


class BaseCategory(BaseModel):
    parent_category  =  models.CharField(max_length=50, choices=CATEGORY)
    category_name = models.CharField(max_length=50)
    category_slug = models.SlugField(max_length=100, unique=True)
    image = models.BinaryField(null=True)

    class Meta:
        db_table = 'coffee_base_category'
        unique_together = ('parent_category', 'category_name', 'is_active', 'is_deleted')   

        

    def __str__(self):
        return f"{self.parent_category}=> {self.category_name}"