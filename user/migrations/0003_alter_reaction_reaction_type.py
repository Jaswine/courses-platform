# Generated by Django 5.0.6 on 2024-06-19 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_reaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reaction',
            name='reaction_type',
            field=models.CharField(choices=[('Like', 'Like'), ('Dislike', 'Dislike'), ('Heart', 'Heart'), ('Unicorn', 'Unicorn'), ('Clap', 'Clap'), ('Fire', 'Fire')], max_length=20),
        ),
    ]