from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email_address = models.CharField(max_length=255, blank=True, null=True)
    mobile_num = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
