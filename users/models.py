from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from .managers import CustomUserManager

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(_('role'), max_length=100, blank=True, null=True)
    department = models.CharField(_('department'), max_length=100, blank=True, null=True)

    user_type = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('teacher', 'Teacher'), ('hod', 'HOD')], default='teacher')

    

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    objects = CustomUserManager()

    def __str__(self):
        return self.email