# Generated by Django 4.2.14 on 2024-11-11 12:13

from django.db import migrations, models
import django.db.models.deletion
import froala_editor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_username'),
        ('school', '0006_remove_lecturevideo_lecture_delete_lectureattachment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='course/cover/'),
        ),
        migrations.AlterField(
            model_name='course',
            name='short_description',
            field=models.CharField(help_text='Please make this a maximum of 220 words', max_length=5000),
        ),
        migrations.AlterField(
            model_name='course',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_category_subcategory', to='school.subcategory'),
        ),
        migrations.AlterField(
            model_name='coursecurriculum',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_curriculum', to='school.course'),
        ),
        migrations.AlterField(
            model_name='coursecurriculum',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_curriculum_profile', to='users.profile'),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='description',
            field=froala_editor.fields.FroalaField(blank=True, help_text='Please make this a maximum of 220 words', max_length=5000),
        ),
    ]
