# Generated by Django 5.2.3 on 2025-06-22 10:31

import users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_first_name_alter_user_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='profile-avatar.jpg', upload_to=users.models.get_random_filename),
        ),
    ]
