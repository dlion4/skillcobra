# Generated by Django 4.2.14 on 2024-11-18 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_profile_purchased_courses'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
