from django.db import models

# ERD -> Company table
# stores all info about company


class Company(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email_address = models.CharField(max_length=255, blank=True, null=True)
    mobile_num = models.CharField(max_length=255, blank=True, null=True)
