import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from core.models import TimeStampedModel, UUIDModel

from .managers import UserManager


class User(PermissionsMixin, UUIDModel, TimeStampedModel, AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_children = models.BooleanField(default=False)

    firstname = models.CharField(max_length=100, default='')
    lastname = models.CharField(max_length=100, default='')

    expo_token = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email


# Create a token when an user is created
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Family(models.Model):
    user = models.ForeignKey(
        User, models.CASCADE)

    def __str__(self):
        return self.user.__str__()


class FamilyMember(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, models.CASCADE)

    def __str__(self):
        return self.user.__str__()
