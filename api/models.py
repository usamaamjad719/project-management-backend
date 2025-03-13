from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings

import uuid
from .managers import (
    DefaultManager,
    VisibleObjectManager,
    NonVisibleObjectManager
)


class UserManager(BaseUserManager):

    use_in_migration = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is Required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'admin'),
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    is_visible = models.BooleanField(default=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, blank=True, null=True)
    username = None
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    visible_objects = VisibleObjectManager()  # Custom manager for visible objects
    non_visible_objects = NonVisibleObjectManager()  # Custom manager for non-visible objects
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return str(self.email)


# base model which all models should inherit if id is a primary key
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    is_visible = models.BooleanField(default=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    objects = DefaultManager()
    visible_objects = VisibleObjectManager()  # Custom manager for visible objects
    non_visible_objects = NonVisibleObjectManager()  # Custom manager for visible objects

    class Meta:
        abstract = True


# base model which all models should inherit if id is not a primary key
class NoIDBaseModel(models.Model):
    is_visible = models.BooleanField(default=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    objects = DefaultManager()
    visible_objects = VisibleObjectManager()  # Custom manager for visible objects
    non_visible_objects = NonVisibleObjectManager()  # Custom manager for visible objects

    class Meta:
        abstract = True


