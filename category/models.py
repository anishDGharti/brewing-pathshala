from django.db import models
from django.utils.text import slugify

from usable.base_models import BaseModel
from usable.constants import CATEGORY

# Create your models here.



class BaseCategory(BaseModel):
    parent_category  =  models.CharField(max_length=50, choices=CATEGORY)
    category_name = models.CharField(max_length=50, unique=True)
    category_slug = models.SlugField(max_length=100, unique=True)
    image = models.BinaryField(null=True)



    def save(self, *args, **kwargs):
        if self.category_slug == "" or self.category_slug == None:
            self.category_slug = slugify(self.category_name) 
        self.category_slug = slugify(self.category_name) 
    
        super(BaseCategory, self).save(*args, **kwargs)


    class Meta:
        db_table = 'coffee_base_category'    