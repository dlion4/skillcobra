# Generated by Django 4.2.14 on 2024-11-12 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0009_alter_course_course_description_alter_course_tutor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='has_free_preview',
            field=models.BooleanField(default=False),
        ),
    ]