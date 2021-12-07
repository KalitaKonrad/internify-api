from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):

    def create_user(self, username, email, user_type, password=None):
        if username is None:
            raise TypeError('Username is empty')
        if email is None:
            raise TypeError('Email is empty')
        if user_type is None:
            raise TypeError('User type is empty')

        user = self.model(username=username, email=self.normalize_email(email))

        if user_type == 'is_company':
            user.is_company = True
        else:
            user.is_employee = True

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, user_type, password=None):
        if password is None:
            raise TypeError('Password is empty')
        if email is None:
            raise TypeError('Email is empty')

        user = self.create_user(username, email, user_type, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.CharField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    is_company = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    # def get_photo_url(self):
    #     return self.photo_url
