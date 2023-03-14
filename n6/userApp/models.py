from django.db import models

from companyApp.models import Company

class UserRole(models.Model):
    role = models.CharField(max_length=255)


# This class defines the User model, which has a first_name, last_name, email_address, company,
# mobile_num, is_active, created_at, and updated_at
class User(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email_address = models.CharField(max_length=255, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    mobile_num = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
