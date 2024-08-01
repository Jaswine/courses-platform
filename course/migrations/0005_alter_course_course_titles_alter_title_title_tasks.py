# Generated by Django 5.0.6 on 2024-07-30 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_rename_tasks_title_title_tasks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_titles',
            field=models.ManyToManyField(blank=True, default=[], related_name='courses', through='course.TitleOrder', to='course.title'),
        ),
        migrations.AlterField(
            model_name='title',
            name='title_tasks',
            field=models.ManyToManyField(blank=True, default=[], related_name='titles', through='course.TaskOrder', to='course.task'),
        ),
    ]