# Generated by Django 4.2.14 on 2024-11-14 10:14

from django.db import migrations, models
import skillcobra.users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_bio_profile_first_name_profile_headline_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=skillcobra.users.models.upload_avatar_to_),
        ),
    ]
