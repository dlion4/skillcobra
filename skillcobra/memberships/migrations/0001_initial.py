# Generated by Django 4.2.14 on 2024-11-15 18:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0005_profile_purchased_courses'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MemberShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('A', 'Active'), ('I', 'Inactive'), ('C', 'Cancelled'), ('P', 'Paused')], default='I', max_length=1)),
            ],
        ),
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
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plan_features', to='memberships.plan')),
            ],
        ),
        migrations.CreateModel(
            name='MemberShipPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=50.0, max_digits=12)),
                ('date_paid', models.DateTimeField(auto_now_add=True)),
                ('payment_method', models.CharField(max_length=50)),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membership_payments', to='memberships.membership')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='users.profile')),
            ],
        ),
        migrations.AddField(
            model_name='membership',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membership_plan', to='memberships.plan'),
        ),
        migrations.AddField(
            model_name='membership',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_membership', to='users.profile'),
        ),
        migrations.CreateModel(
            name='FeatureAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False)),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='memberships.feature')),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='memberships.membershippayment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
    ]
