from django.db import models
from userApp.models import UserRole, User
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, user_name, user_level, user, password=None, password2=None):
        """
        It creates a user, saves the user, and returns the user
        
        :param user_name: The user_name of the user
        :param user_level: This is the level of the user
        :param user: The user model to use for the user
        :param password: The password to be used for the user
        :param password2: This is the second password field that the user will fill out
        :return: The data is being returned.
        """
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
        """
        It creates a user, and then sets the user's is_admin attribute to True
        
        :param user_name: The username of the user
        :param user_level: This is the level of the user
        :param user: The user object that is being created
        :param password: The password for the user
        :param password2: This is the second password field that we will use to confirm the password
        :return: The data is being returned.
        """
        data = self.create_user(
            user_name,
            password=password,
            user_level=user_level,
            user=user,
        )
        data.is_admin = True
        data.save(using=self._db)
        return data

 
# The Credential class

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
    
    def __str__(self):
        return self.user_name


    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
