# Generated by Django 5.1.2 on 2024-11-13 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tags',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
