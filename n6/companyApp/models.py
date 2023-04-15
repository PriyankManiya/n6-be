from django.db import models

# This class defines a company, which has a name, email address, mobile number, and a boolean value
# indicating whether or not the company is active
class Company(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email_address = models.CharField(max_length=255, blank=True, null=True)
    mobile_num = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
