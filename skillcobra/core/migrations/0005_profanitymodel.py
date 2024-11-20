# Generated by Django 4.2.14 on 2024-11-19 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfanityModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=100)),
                ('profanity_score', models.PositiveBigIntegerField(default=0)),
            ],
        ),
    ]