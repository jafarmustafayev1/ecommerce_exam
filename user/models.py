# ----------------------------------------------------------------
from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
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

        # Email yuborish
        send_mail(
            'Email Address Update',
            f'Your email address is being updated to: {instance.email}',
            'muzaffaribrohimov7777@gmail.com',
            [instance.email],
            fail_silently=False,
        )


# post_save signal: yangi foydalanuvchi yaratildimi yoki yangilanganmi
@receiver(post_save, sender=User)
def after_save_user(sender, instance, created, **kwargs):
    if created:
        message = f"Yangi foydalanuvchi yaratildi: {instance.email}"
    else:
        message = f"Foydalanuvchi yangilandi: {instance.email}"

    # Email yuborish foydalanuvchi yaratildi yoki yangilandi
    send_mail(
        'User Created or Updated',
        message,
        'muzaffaribrohimov7777@gmail.com',
        [instance.email],
        fail_silently=False,
    )


# pre_delete signal: foydalanuvchi o'chirilishidan oldin
@receiver(pre_delete, sender=User)
def before_delete_user(sender, instance, **kwargs):
    message = f"Foydalanuvchi o'chirilmoqda: {instance.email}"

    # Email yuborish foydalanuvchi o'chirilishidan oldin
    send_mail(
        'User Deletion Warning',
        message,
        'muzaffaribrohimov7777@gmail.com',
        [instance.email],
        fail_silently=False,
    )


# post_delete signal: foydalanuvchi o'chirilgandan keyin
@receiver(post_delete, sender=User)
def after_delete_user(sender, instance, **kwargs):
    message = f"Foydalanuvchi o'chirildi: {instance.email}"

    # Email yuborish foydalanuvchi o'chirilgandan keyin
    send_mail(
        'User Deleted',
        message,
        'muzaffaribrohimov7777@gmail.com',
        [instance.email],
        fail_silently=False,
    )
