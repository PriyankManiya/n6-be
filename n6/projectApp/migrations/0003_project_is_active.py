# Generated by Django 4.1.4 on 2023-03-03 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectApp', '0002_project_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
