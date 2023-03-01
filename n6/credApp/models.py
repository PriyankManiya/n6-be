from django.db import models
from userApp.models import UserRole, User

# Create your models here.

# ERD -> Credential
# stores all credential information for the user accounts
# TODO change password field data type for encryption
class Credential(models.Model):
    user_level = models.ForeignKey(
        UserRole, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    active_tf = models.BooleanField(blank=True, null=True, default=True)
