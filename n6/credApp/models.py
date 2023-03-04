from django.db import models
from userApp.models import UserRole, User
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, user_name, user_level, user, password=None, password2=None):
        if not user_name:
            raise ValueError('Users must have an user_name ')

        data = self.model(
            user_name=user_name,
            user_level=user_level,
            user=user,
        )

        data.set_password(password)
        data.save(using=self._db)
        return data

    def create_superuser(self, user_name, user_level, user, password=None, password2=None):
        data = self.create_user(
            user_name,
            password=password,
            user_level=user_level,
            user=user,
        )
        data.is_admin = True
        data.save(using=self._db)
        return data


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
    
    objects = UserManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['user_level', 'user', 'password', 'is_active']

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_active(self, perm, obj=None):
        return self.is_active
