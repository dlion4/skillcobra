# Generated by Django 4.2.14 on 2024-11-16 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0009_alter_payoutaccount_account_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payoutaccount',
            name='account_type',
            field=models.CharField(choices=[('paypal', 'Paypal Account'), ('mpesa', 'MPesa Account'), ('airtel', 'Airtel Account'), ('bank', 'Bank Account')], default='bank', max_length=10),
        ),
    ]
