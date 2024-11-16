# Generated by Django 4.2.14 on 2024-11-16 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0007_billingaddress_payoutaccount_paypalaccount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payoutaccount',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='payoutaccount',
            name='object_id',
        ),
        migrations.AlterField(
            model_name='mpesaaccount',
            name='payout_account',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mpesa_account', to='payments.payoutaccount'),
        ),
        migrations.AlterField(
            model_name='payoutaccount',
            name='account_type',
            field=models.CharField(choices=[('paypal', 'Paypal Account'), ('mpesa', 'MPesa Account'), ('airtel', 'Airtel Account'), ('bank', 'Bank Account')], default='bank', max_length=10),
        ),
        migrations.CreateModel(
            name='AirtelAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=100)),
                ('payout_account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='airtel_account', to='payments.payoutaccount')),
            ],
        ),
    ]
