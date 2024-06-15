# Generated by Django 5.0.6 on 2024-06-11 07:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='views',
            field=models.ManyToManyField(blank=True, related_name='articleViews', to=settings.AUTH_USER_MODEL),
        ),
    ]