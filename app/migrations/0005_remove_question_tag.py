# Generated by Django 5.1.3 on 2024-11-18 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_question_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='tag',
        ),
    ]
