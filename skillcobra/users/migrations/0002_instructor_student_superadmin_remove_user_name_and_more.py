# Generated by Django 4.2.14 on 2024-11-07 16:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import skillcobra.users.managers


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instructor',
            fields=[
            ],
            options={
                'verbose_name': 'Instructor',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
            managers=[
                ('objects', skillcobra.users.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
            ],
            options={
                'verbose_name': 'Student',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
            managers=[
                ('objects', skillcobra.users.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='SuperAdmin',
            fields=[
            ],
            options={
                'verbose_name': 'SuperAdmin',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
            managers=[
                ('objects', skillcobra.users.managers.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('student', 'Student'), ('instructor', 'Instructor'), ('superadmin', 'SuperAdmin')], default='student', max_length=20),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
