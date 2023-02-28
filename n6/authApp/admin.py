from django.contrib import admin
from authApp.models import Company, Credential, User, UserRole
# Register your models here.
admin.site.register(User)
admin.site.register(Credential)
admin.site.register(UserRole)
admin.site.register(Company)