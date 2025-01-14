# Generated by Django 4.2.17 on 2025-01-12 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='question',
            name='avatar',
            field=models.ImageField(blank=True, default='questions_avatars/default.jpg', null=True, upload_to='questions_avatars/'),
        ),
    ]
