from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# ERD -> User_Level table
# stores all roles for the user accounts
class UserRole(models.Model):
    role = models.CharField(max_length=255)


# ERD -> Company table
# stores all info about company
class Company(models.Model):
    name = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    mobile_num = models.CharField(max_length=255, default=None, blank=True, null=True)

    def create_company(self, name, email_address, mobile_num):

        company = self.model(
            email_address=email_address,
            name=name,
            mobile_num=mobile_num,
        )

        company.save()
        return company



# ERD -> User table
# stores all user details for user account
# TODO add company foreign key after company table has been created
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    mobile_num = models.CharField(max_length=255)


# ERD -> Credential
# stores all credential information for the user accounts
# TODO change password field data type for encryption
class Credential(models.Model):
    user_level = models.ForeignKey(UserRole, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    active_tf = models.BooleanField()
