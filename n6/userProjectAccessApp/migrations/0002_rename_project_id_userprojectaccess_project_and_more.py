# Generated by Django 4.1.4 on 2023-03-03 22:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('userProjectAccessApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprojectaccess',
            old_name='project_id',
            new_name='project',
        ),
        migrations.RenameField(
            model_name='userprojectaccess',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='userprojectaccess',
            name='access_url_updated_at',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprojectaccess',
            name='otp_updated_at',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
