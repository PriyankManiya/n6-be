from django.contrib import admin
from .models import Credential, User, UserRole
# Register your models here.

admin.site.register(User)
admin.site.register(Credential)
admin.site.register(UserRole)
