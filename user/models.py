# from django.db import models
# from .managers import UserManager
# from django.contrib.auth.models import AbstractUser
#
# # Create your models here.
# class User(AbstractUser):
#   username = None
#   email = models.EmailField(
#         "Email Address",
#         unique=True,
#     )
#   USERNAME_FIELD = 'email'
#   REQUIRED_FIELDS = []
#   objects = UserManager()
#
#   def __str__(self):
#       return self.email

from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

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

  # pre_save signal: emailni kichik harflarga o'zgartirish
@receiver(pre_save, sender=User)
def before_save_email(sender, instance, **kwargs):
      if instance.email:
          instance.email = instance.email.lower()

  # post_save signal: yangi foydalanuvchi yaratildimi yoki yangilanganmi
@receiver(post_save, sender=User)
def after_save_user(sender, instance, created, **kwargs):
      if created:
          print(f"Yangi foydalanuvchi yaratildi: {instance.email}")
      else:
          print(f"Foydalanuvchi yangilandi: {instance.email}")

  # pre_delete signal: foydalanuvchi o'chirilishidan oldin
@receiver(pre_delete, sender=User)
def before_delete_user(sender, instance, **kwargs):
      print(f"Foydalanuvchi o'chirilmoqda: {instance.email}")

  # post_delete signal: foydalanuvchi o'chirilgandan keyin
@receiver(post_delete, sender=User)
def after_delete_user(sender, instance, **kwargs):
      print(f"Foydalanuvchi o'chirildi: {instance.email}")
