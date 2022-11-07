from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Local imports
from .managers import CustomUserManager

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    
    manager = CustomUserManager()
