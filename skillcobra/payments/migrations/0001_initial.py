# Generated by Django 4.2.14 on 2024-11-10 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('B', 'Basic'), ('P', 'Pro')], default='B', max_length=1, unique=True)),
                ('price', models.DecimalField(decimal_places=2, default=10.5, max_digits=10)),
                ('duration', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='PlanFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.CharField(max_length=100, unique=True)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plan_features', to='payments.plan')),
            ],
        ),
        migrations.CreateModel(
            name='MemberShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('A', 'Active'), ('I', 'Inactive'), ('C', 'Cancelled'), ('P', 'Paused')], default='I', max_length=1)),
                ('is_paid', models.BooleanField(default=False)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membership_plan', to='payments.plan')),
            ],
        ),
    ]