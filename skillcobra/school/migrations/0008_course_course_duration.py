# Generated by Django 4.2.14 on 2024-11-11 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0007_course_cover_alter_course_short_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_duration',
            field=models.CharField(default='1 hour 3 minutes', help_text='Approximate duration of the course. Can be in weeks, days or even hours', max_length=300),
        ),
    ]
