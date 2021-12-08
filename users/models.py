from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    jobs_applied = models.ManyToManyField("job_listings.Job", blank=True)


# this is being called every time any changes are made to the user model
@receiver(post_save, sender=User)
def create_link_to_user_after_user_created(sender, instance, **kwargs):
    # this throws an exception when employee not found -> we want to assign employee object only once
    # and the whole function is being called during every User update (save() method call)
    try:
        employee = Employee.objects.get(user=instance)
    except:
        user = User.objects.get(id=instance.id)
        employee = Employee(user=user)
        employee.save()
