from django.db import models
from noteApp.models import Note


# The Attachment class is a model that has a foreign key to the Note class, a filename, a path, a
# boolean field, and two date time fields
class Attachment(models.Model):
    note = models.ForeignKey(
        Note, on_delete=models.CASCADE, blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True, null=True)
    path = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
