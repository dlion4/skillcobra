# Generated by Django 4.2.14 on 2024-11-10 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('school', '0003_coursecurriculum_tutor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursecurriculum',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='course_curriculum', to='school.course'),
        ),
        migrations.AlterField(
            model_name='coursecurriculum',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='course_curriculum_profile', to='users.profile'),
        ),
    ]