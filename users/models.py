from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.conf import settings
from .managers import CustomUserManager
from users.utils import resize_image_to_square

class Department(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name.title()
    
def image_directory_path(instance, filename):
    print(filename)
    return 'images_{0}/{1}'.format(instance, filename)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_working = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    employee_id = models.CharField(max_length=20, unique=True)
    position = models.CharField(max_length=120, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    contact = models.CharField(max_length=13, blank=True)
    image = models.ImageField(upload_to=image_directory_path, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if self.image:
            self.image = resize_image_to_square(self.image, 300)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
