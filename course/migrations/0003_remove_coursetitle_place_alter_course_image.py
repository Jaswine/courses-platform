# Generated by Django 4.1.7 on 2023-04-17 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_course_coursetask_taskcomment_coursetitle_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursetitle',
            name='place',
        ),
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, upload_to='courses'),
        ),
    ]
