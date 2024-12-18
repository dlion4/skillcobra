# Generated by Django 4.2.14 on 2024-11-16 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0006_remove_planfeature_plan_delete_membership_and_more'),
        ('instructor', '0002_remove_coursesale_transactions'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursesale',
            name='transactions',
            field=models.ManyToManyField(blank=True, related_name='course_sales', to='payments.transaction'),
        ),
    ]
