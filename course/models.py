from django.db import models
from django.utils.text import slugify
from category.models import BaseCategory
from usable.base_models import BaseModel
from usable.constants import CLASS_TYPE_CHOICES,  LANGUAGE, LEVEL

# Create your models here.






class PhysicalCourse(BaseModel):

    course_category = models.ForeignKey(BaseCategory, on_delete=models.SET_NULL, null=True, blank=True)
    course_name = models.CharField(max_length=100)
    course_description = models.TextField(null=True, blank=True)
    image = models.BinaryField(null=True)
    course_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    course_language = models.CharField(choices=LANGUAGE, default="English", max_length=100)
    course_difficulty_level = models.CharField(choices=LEVEL, default="Beginner", max_length=100)
    course_duration = models.DurationField()
    course_class_type = models.CharField(choices=CLASS_TYPE_CHOICES, default='Regular', max_length=20)
    cours_slug = models.SlugField(unique=True, max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'coffee_physical_course'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(PhysicalCourse, self).save(*args, **kwargs)

    def get_duration_display(self):
        """ Returns the duration in a human-readable format based on duration_format """
        if self.duration_format == 'days':
            return f"{self.duration.days} day{'s' if self.duration.days > 1 else ''}"
        else:  # Assuming hours
            total_hours = self.duration.total_seconds() // 3600
            return f"{int(total_hours)} hour{'s' if total_hours > 1 else ''}"