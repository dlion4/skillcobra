# Generated by Django 4.2.14 on 2024-11-11 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0005_alter_lecture_lecture_video_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecturevideo',
            name='lecture',
        ),
        migrations.DeleteModel(
            name='LectureAttachment',
        ),
        migrations.DeleteModel(
            name='LectureVideo',
        ),
    ]
