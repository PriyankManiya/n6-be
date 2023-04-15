# n6-be
n6-be


# To import list of package into file, hit the below command

- `pip freeze > requirements.txt`

# To install all the package in your env, hit below command

- `pip install -r requirements.txt`

# Convert Models into tables in DB

- `python3 manage.py migrate`

# Migration of App

- `python3 manage.py makemigrations {app_name}`

# Migrate Models into tables in DB

- `python3 manage.py migrate`

### SQL Migration with migration process name

- `python3 manage.py sqlmigrate {app_name} 0001`

- The **`[sqlmigrate](https://docs.djangoproject.com/en/4.1/ref/django-admin/#django-admin-sqlmigrate)`** command doesn’t actually run the migration on your database - instead, it prints it to the screen so that you can see what SQL Django thinks is required. It’s useful for checking what Django is going to do or if you have database administrators who require SQL scripts for changes.

- Change your models (in **`models.py`**).

- Run **`[python manage.py makemigrations](https://docs.djangoproject.com/en/4.1/ref/django-admin/#django-admin-makemigrations)`** to create migrations for those changes
- Run **`[python manage.py migrate](https://docs.djangoproject.com/en/4.1/ref/django-admin/#django-admin-migrate)`** to apply those changes to the database.
