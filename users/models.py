from django.db import models
from django.contrib.auth.models import AbstractUser

SEX_CHOICES = (
    ("M", "Male"),
    ("F", "Female")
)

ROLES_CHOICES = (
    ('SA','Super Admin'),
    ('A', 'Admin'),
    ('M', "Manager"),
    ('S', "Supervisor")
)

class CustomUser(AbstractUser):
    pass

class AdminUser(CustomUser):
    # this admin user will contain
    # username, firstname, last name , email, password
    user_role = models.CharField(choices=ROLES_CHOICES, max_length=2)
    full_name = models.CharField(max_length=80, default="")
    phone_number = models.CharField(max_length=20, default="")

    # required in login form
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name_plural = "Dashboard Users"

class AppUser(CustomUser):
    # this app user will contain
    # username, firstname, lastname, email, password

    # visible to other users
    bio = models.CharField(max_length=80)
    show_bio = models.BooleanField(default=True)
    is_registerd = models.BooleanField(default=False)
    is_certified = models.BooleanField(default=False)
    image = models.ImageField()

    # not visible to others users, used for adver
    age = models.PositiveIntegerField()
    sex = models.CharField(choices=SEX_CHOICES, max_length=1)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)

    # for manager and supervisor
    followers = models.PositiveIntegerField(default=0)
    register_date = models.DateTimeField()
    last_view_date = models.DateTimeField()
    last_login_date = models.DateTimeField()
    ip = models.GenericIPAddressField()
    is_blocked = models.BooleanField(default=False)
    block_time = models.DateTimeField()

    class Meta:
        verbose_name_plural = "App Users"
