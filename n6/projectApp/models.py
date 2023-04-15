from django.db import models
from companyApp.models import Company
from userApp.models import User

# The Project class is a model that has a foreign key to the Company class, a name, a description, a
# boolean field, and two date time fields
class Project(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, 
        # related_name='projects',
        blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)