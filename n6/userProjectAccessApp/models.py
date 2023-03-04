from django.db import models

from userApp.models import User
from projectApp.models import Project


class UserProjectAccess(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, blank=True, null=True)
    access_url = models.CharField(max_length=255, blank=True, null=True)
    otp = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    otp_updated_at = models.DateTimeField(auto_now=True)
    access_url_updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
