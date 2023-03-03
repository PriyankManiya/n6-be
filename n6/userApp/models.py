from django.db import models

from companyApp.models import Company

# ERD -> User_Level table
# stores all roles for the user accounts


class UserRole(models.Model):
    role = models.CharField(max_length=255)


# ERD -> User table
# stores all user details for user account
# TODO add company foreign key after company table has been created
class User(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email_address = models.CharField(max_length=255, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    mobile_num = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
