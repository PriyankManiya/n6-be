from django.db import models
from projectApp.models import Project
from userApp.models import User


# A Note is a message that a user can send to another user or to a project
class Note(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    responded_note = models.IntegerField(blank=True, null=True, default=0)
    topic = models.CharField(max_length=255, blank=True, null=True)
    content_html = models.TextField(blank=True, null=True)
    read_tf = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
