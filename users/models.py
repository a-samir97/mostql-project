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
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class AdminUser(CustomUser):
    # this admin user will contain
    # username, firstname, last name , email, password
    user_id = models.AutoField(primary_key=True)
    user_role = models.CharField(choices=ROLES_CHOICES, max_length=2)
    full_name = models.CharField(max_length=80, default="")
    phone_number = models.CharField(max_length=20, default="")

    class Meta:
        verbose_name_plural = "Dashboard Users"

class AppUser(CustomUser):
    # this app user will contain
    # username, firstname, lastname, email, password
    
    user_id = models.AutoField(primary_key=True)    
    
    # if user registered
        # should appear in search
        # should have a web page
        # should have qr code
        # should have profile pic

    # authentication using facebook and google
    user_token = models.CharField(max_length=40, null=True, blank=True)

    # visible to other users
    
    name_id = models.CharField(unique=True, max_length=40)
    bio = models.CharField(max_length=80, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    qr_code = models.ImageField(null=True, blank=True)
    nickname = models.CharField(max_length=30, null=True, blank=True)

    # Bool Fields  
    show_bio = models.BooleanField(default=True)
    is_registerd = models.BooleanField(default=False)
    is_certified = models.BooleanField(default=False)
    visible_in_search = models.BooleanField(default=True)
    receive_email = models.BooleanField(default=False)      
    

    # not visible to others users, used for adver
    age = models.PositiveIntegerField()
    sex = models.CharField(choices=SEX_CHOICES, max_length=1)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)


    # for manager and supervisor
    followers = models.PositiveIntegerField(default=0)
    
    register_date = models.DateTimeField(null=True, blank=True)
    last_view_date = models.DateTimeField(null=True, blank=True)
    last_login_date = models.DateTimeField(null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    
    is_blocked = models.BooleanField(default=False)
    block_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.user_id)

    USERNAME_FIELD = 'name_id'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name_plural = "App Users"
