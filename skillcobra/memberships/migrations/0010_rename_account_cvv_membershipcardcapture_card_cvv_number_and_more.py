# Generated by Django 4.2.14 on 2024-11-17 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0009_membershipcardcapture'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membershipcardcapture',
            old_name='account_cvv',
            new_name='card_cvv_number',
        ),
        migrations.RenameField(
            model_name='membershipcardcapture',
            old_name='account_name',
            new_name='card_holder_name',
        ),
    ]
