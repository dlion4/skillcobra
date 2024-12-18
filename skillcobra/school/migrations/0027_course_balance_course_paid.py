# Generated by Django 4.2.14 on 2024-11-20 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0026_alter_category_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
        migrations.AddField(
            model_name='course',
            name='paid',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
    ]
