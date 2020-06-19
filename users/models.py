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

LOGIN_VIA = (
    ('F', 'Facebook'),
    ('G', 'Google'),
    ('N', 'None')
)

class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        if self.username:
            return str(self.username)
        elif self.email:
            return str(self.email)
        return str(self.id)
    
    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = []

class AdminUser(CustomUser):
    # this admin user will contain
    # username, firstname, last name , email, password
    user_role = models.CharField(choices=ROLES_CHOICES, max_length=2)
    full_name = models.CharField(max_length=80, default="")
    phone_number = models.CharField(max_length=20, default="")
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
        
    class Meta:
        verbose_name_plural = "Dashboard Users"







class Accounts(models.Model):

    phone = models.CharField(max_length=50, null=True, blank=True)
    phone_visible = models.BooleanField(default=True)
    
    website = models.CharField(max_length=50, null=True, blank=True)
    website_visible = models.BooleanField(default=True)

    whatsapp = models.CharField(max_length=50, null=True, blank=True)
    whatsapp_visible = models.BooleanField(default=True)

    facebook = models.CharField(max_length=50, null=True, blank=True)
    facebook_visible = models.BooleanField(default=True)

    instgram = models.CharField(max_length=50, null=True, blank=True)
    instgram_visible = models.BooleanField(default=True)

    gmail = models.CharField(max_length=50, null=True, blank=True)
    gmail_visible = models.BooleanField(default=True)

    youtube = models.CharField(max_length=50, null=True, blank=True)
    youtube_visible = models.BooleanField(default=True)

    linkedin = models.CharField(max_length=50, null=True, blank=True)
    linkedin_visible = models.BooleanField(default=True)

    twitter = models.CharField(max_length=50, null=True, blank=True)
    twitter_visible = models.BooleanField(default=True)

    snapchat = models.CharField(max_length=50, null=True, blank=True)
    snapchat_visible = models.BooleanField(default=True)



class AppUser(CustomUser):

    # if user registered
        # should appear in search
        # should have a web page
        # should have qr code
        # should have profile pic

    # authentication using facebook and google
    user_token = models.CharField(max_length=40, null=True, blank=True)
    login_via = models.CharField(max_length=2, choices=LOGIN_VIA, default='N')

    # visible to other users
    name_id = models.CharField(unique=True, max_length=40)
    bio = models.CharField(max_length=80, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    qr_code = models.ImageField(null=True, blank=True, upload_to='qrcodes/')
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
    register_date = models.DateTimeField(null=True, blank=True)
    last_view_date = models.DateTimeField(null=True, blank=True)
    last_login_date = models.DateTimeField(null=True, blank=True)

    # user ip information 
    first_ip = models.GenericIPAddressField(null=True, blank=True)
    ip_sign_in_today = models.GenericIPAddressField(null=True, blank=True)

    is_blocked = models.BooleanField(default=False)
    block_time = models.DateTimeField(null=True, blank=True)

    # following system
    friends_list = models.ManyToManyField('AppUser', related_name='friends', blank=True)
    status_list = models.ManyToManyField('AppUser', related_name='waiting_list', blank=True)

    # user accounts 
    accounts = models.OneToOneField(Accounts, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name_id

    USERNAME_FIELD = 'name_id'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name_plural = "App Users"
