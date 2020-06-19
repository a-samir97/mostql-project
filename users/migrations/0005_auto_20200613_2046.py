# Generated by Django 3.0 on 2020-06-13 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200608_2230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appuser',
            name='followers',
        ),
        migrations.AddField(
            model_name='appuser',
            name='friends_list',
            field=models.ManyToManyField(related_name='friends', to='users.AppUser'),
        ),
        migrations.AddField(
            model_name='appuser',
            name='status_list',
            field=models.ManyToManyField(related_name='waiting_list', to='users.AppUser'),
        ),
    ]
