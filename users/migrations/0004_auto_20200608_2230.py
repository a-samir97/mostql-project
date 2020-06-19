# Generated by Django 3.0 on 2020-06-08 19:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_adminuser_is_blocked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminuser',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='appuser',
            name='user_id',
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='customuser_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='customuser_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
