# Generated by Django 5.0.3 on 2024-04-27 01:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0003_movies_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='description',
        ),
    ]