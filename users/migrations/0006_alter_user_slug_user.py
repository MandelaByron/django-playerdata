# Generated by Django 5.2.3 on 2025-06-22 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_slug_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='slug_user',
            field=models.SlugField(max_length=30, null=True, unique=True),
        ),
    ]
