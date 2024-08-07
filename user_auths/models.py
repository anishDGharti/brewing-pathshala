from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.db import models
from usable.base_models import BaseModel 
from django.db.models import Q, UniqueConstraint
from django.utils.translation import gettext_lazy as _
# Create your models here.

from django.dispatch import receiver


GENDER_OPTIONS = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    )

STATE_CHOICES = (
    ("koshi", "Koshi"),
    ("madhesh", "Madhesh"),
    ("bagmati", "Bagmati"),
    ("gandaki", "Gandaki"),
    ("lumbini", "Lumbini"),
    ("karnali", "Karnali"),
    ("sudurpaschim", "Sudurpaschim"),
)




class UserManager(BaseUserManager):
    def create_user(self,  username, email, phone_number, password=None):
        if not email:
            raise ValueError("User must have an email address.")
        
        if not username:
            raise ValueError("User must have a username to continue.")

        if not phone_number:
            raise ValueError("User must have a phone number to continue.")


        user = self.model(
            email = self.normalize_email(email),
            phone_number=phone_number,
            username=username, 
        )    
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,  username, email,phone_number, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            phone_number = phone_number,
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    



class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    first_name = models.CharField(max_length=20, blank=True, null=True, help_text="First name of the user")
    last_name = models.CharField(max_length=20, blank=True, null=True, help_text="Last name of the user")
    username = models.CharField(max_length=50, unique=True, error_messages={"unique": "Username must be set"}, help_text="Unique username of the user")
    email = models.EmailField(max_length=50, unique=True, error_messages={"unique": "Email must be provided"}, help_text="Email address of the user")
    phone_number = models.CharField(max_length=10, null=False, unique=True, error_messages={"null": "Phone Number must be Provided"}, help_text="Phone number of the user")
   
    # profile fields
   
    address = models.CharField(max_length=255, blank=True, null=True, help_text="Address of the user (e.g., Tilottama-3, Yogikuti, Shantichowk, near futsal Brahmapath)")
    city = models.CharField(max_length=50, blank=True, null=True, help_text="City of residence")
    district = models.CharField(max_length=50, blank=True, null=True, help_text="City of residence")
    state = models.CharField(max_length=20, choices=STATE_CHOICES, blank=True, null=True)    
    profile_picture = models.ImageField(upload_to='profile_images/', blank=True, null=True, help_text="Profile picture of the user")
    gender = models.CharField(max_length=10, blank=True, help_text="Gender of the user")
    date_of_birth = models.DateField(null=True, blank=True, help_text="Date of birth of the user")
    
    # required fields
    access_token = models.CharField(max_length=32, unique=True, null=True, help_text="Access token for the user")
    password = models.CharField(_("password"), max_length=128, help_text="Password for the user account")
   
    date_joined = models.DateTimeField(auto_now_add=True, help_text="Date when the user joined")
    is_staff = models.BooleanField(default=False, help_text="Status to check if the user is a staff member")  # Add this line
    is_student = models.BooleanField(default=False, help_text="Status to check if the user is a student")
    


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    objects = UserManager()

    class Meta:
        db_table = "coffee_users"
        indexes = [
            models.Index(fields=['username'], name='idx_users_username'),
            models.Index(fields=['email'], name='idx_users_email'),
            models.Index(fields=['phone_number'], name='idx_users_phone_number'),
        ]
        constraints = [
            UniqueConstraint(
                fields=['phone_number'],
                condition=Q(is_active=True),
                name='unique_active_phone_number'
            ),
            UniqueConstraint(
                fields=['email'],
                condition=Q(is_active=True),
                name='unique_active_email'
            ),
            UniqueConstraint(
                fields=['username'],
                condition=Q(is_active=True),
                name='unique_active_username'
            ),
        ]
     


    def __str__(self):
        return self.email


    def has_module_perms(self, app_label):
        return True







class Menu(BaseModel):
    menu_name = models.CharField(max_length=200)
    parent = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True,related_name="+")
    ordinal_number  = models.IntegerField(default=0)
    roles = models.ManyToManyField(Group, blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)
    url = models.CharField(max_length=200)  
    icon = models.CharField(max_length=100, blank=True, null=TabError)

    class Meta:
        db_table = 'coffee_menu'



class Education(BaseModel):
    FACULTY_CHOICES = [
        ('Science', 'Science'),
        ('Management', 'Management'),
    ]

    STATUS_CHOICES = [
        ('Running', 'Running'),
        ('Completed', 'Completed'),
    ]

    student = models.ForeignKey(User, related_name='education', on_delete=models.CASCADE)
    institute_name = models.CharField(max_length=255, blank=True, null=True, help_text="Name of the institute")
    faculty = models.CharField(max_length=50, choices=FACULTY_CHOICES, blank=True, null=True)
    level = models.CharField(max_length=10, choices=[
        ('10', '10'),
        ('10+2', '10+2'),
        ('Bachelor', 'Bachelor'),
        ('Masters', 'Masters'),
    ], blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "coffee_education"
       
    def __str__(self):
        return f"Education for {self.student.username}"    