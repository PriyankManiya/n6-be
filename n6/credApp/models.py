from django.db import models
from userApp.models import UserRole, User
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

# ERD -> Credential
# stores all credential information for the user accounts
# TODO change password field data type for encryption


# class UserManager(BaseUserManager):
#     def create_user(self, email, name, tc, password=None, password2=None):
#         # """
#         # Creates and saves a User with the given email, name, tc and password.
#         # """
#         # if not email:
#         #     raise ValueError('Users must have an email address')

#         # user = self.model(
#         #     email=self.normalize_email(email),
#         #     name=name,
#         #     tc=tc,
#         # )

#         # user.set_password(password)
#         # user.save(using=self._db)
#         return user

#     def create_superuser(self, email, name, tc, password=None, password2=None):
#         """
#         Creates and saves a superuser with the given email, name, tc and password.
#         """
#         user = self.create_user(
#             email,
#             password=password,
#             name=name,
#             tc=tc,
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user


class Credential(AbstractBaseUser):
    user_level = models.ForeignKey(
        UserRole, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    user_name = models.CharField(
        max_length=255, unique=True,
    )
    password = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['user_level', 'user', 'password', 'is_active']
