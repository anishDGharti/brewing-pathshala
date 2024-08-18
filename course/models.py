from django.db import models
from django.utils.text import slugify
from usable.base_models import BaseModel
from usable.constants import CLASS_TYPE_CHOICES, DURATION_FORMAT_CHOICES, LANGUAGE, LEVEL

# Create your models here.


class CourseCategory(BaseModel):
    title = models.CharField(max_length=50, error_messages="Coffee Course Category cannot be blank")
    image = models.BinaryField(null=True)
    slug = models.SlugField(unique=True, max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.title) 
        super(CourseCategory, self).save(*args, **kwargs)


    class Meta:
        db_table = 'coffee_course_category'




class PhysicalCourse(BaseModel):

    category = models.ForeignKey(CourseCategory, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    image = models.BinaryField(null=True)

    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    language = models.CharField(choices=LANGUAGE, default="English", max_length=100)
    difficulty_level = models.CharField(choices=LEVEL, default="Beginner", max_length=100)
    duration = models.DurationField()
    duration_format = models.CharField(choices=DURATION_FORMAT_CHOICES, default='hours', max_length=10)
    class_type = models.CharField(choices=CLASS_TYPE_CHOICES, default='regular', max_length=10)
    slug = models.SlugField(unique=True, max_length=200, blank=True, null=True)

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