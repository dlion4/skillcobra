# Generated by Django 4.2.14 on 2024-11-19 16:14

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0006_alter_coupon_students'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='coupon',
            managers=[
                ('admin_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]