# Generated by Django 2.1 on 2020-05-28 20:35

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to=settings.AUTH_USER_MODEL)),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_role', models.CharField(choices=[('SA', 'Super Admin'), ('A', 'Admin'), ('M', 'Manager'), ('S', 'Supervisor')], max_length=2)),
                ('full_name', models.CharField(default='', max_length=80)),
                ('phone_number', models.CharField(default='', max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Dashboard Users',
            },
            bases=('users.customuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to=settings.AUTH_USER_MODEL)),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('bio', models.CharField(max_length=80)),
                ('show_bio', models.BooleanField(default=True)),
                ('is_registerd', models.BooleanField(default=False)),
                ('is_certified', models.BooleanField(default=False)),
                ('image', models.ImageField(upload_to='')),
                ('age', models.PositiveIntegerField()),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('country', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('followers', models.PositiveIntegerField(default=0)),
                ('register_date', models.DateTimeField()),
                ('last_view_date', models.DateTimeField()),
                ('last_login_date', models.DateTimeField()),
                ('ip', models.GenericIPAddressField()),
                ('is_blocked', models.BooleanField(default=False)),
                ('block_time', models.DateTimeField()),
            ],
            options={
                'verbose_name_plural': 'App Users',
            },
            bases=('users.customuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
