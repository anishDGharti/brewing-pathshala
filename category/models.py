from django.db import models
from django.utils.text import slugify

from usable.base_models import BaseModel
from usable.constants import CATEGORY

# Create your models here.



class BaseCategory(BaseModel):
    parent_category  =  models.CharField(max_length=50, choices=CATEGORY)
    category_name = models.CharField(max_length=50)
    category_slug = models.SlugField()
    image = models.BinaryField(null=True)



    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.title) 
        super(BaseCategory, self).save(*args, **kwargs)


    class Meta:
        db_table = 'coffee_base_category'    