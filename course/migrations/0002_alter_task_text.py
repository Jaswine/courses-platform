# Generated by Django 4.2.5 on 2023-09-30 05:21

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='text',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
    ]