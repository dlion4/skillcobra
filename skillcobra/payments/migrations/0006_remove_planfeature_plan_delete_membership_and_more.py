# Generated by Django 4.2.14 on 2024-11-15 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_transaction_account_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planfeature',
            name='plan',
        ),
        migrations.DeleteModel(
            name='MemberShip',
        ),
        migrations.DeleteModel(
            name='Plan',
        ),
        migrations.DeleteModel(
            name='PlanFeature',
        ),
    ]
