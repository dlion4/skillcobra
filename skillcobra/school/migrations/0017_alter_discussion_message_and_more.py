# Generated by Django 4.2.14 on 2024-11-13 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0016_discussionreply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussion',
            name='message',
            field=models.CharField(max_length=3000),
        ),
        migrations.AlterField(
            model_name='discussionreply',
            name='message',
            field=models.CharField(max_length=3000),
        ),
    ]
