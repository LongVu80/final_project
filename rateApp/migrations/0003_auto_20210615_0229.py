# Generated by Django 2.2 on 2021-06-15 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rateApp', '0002_delete_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Like',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='likes',
            new_name='user_likes',
        ),
        migrations.RemoveField(
            model_name='message',
            name='likes',
        ),
        migrations.AddField(
            model_name='message',
            name='user_likes',
            field=models.ManyToManyField(related_name='user_likes', to='rateApp.User'),
        ),
    ]
