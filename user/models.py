from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
  username = None
  email = models.EmailField(
        "Email Address",
        unique=True,
    )
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []
  objects = UserManager()

  def __str__(self):
      return self.email