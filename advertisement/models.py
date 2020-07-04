from django.db import models
from users.models import AdminUser

SEX_CHOICES = (
    ("M", "Male"),
    ("F", "Female")
)
class Advertising(models.Model):

    image = models.ImageField()
    url = models.URLField()
    start_date = models.DateField()
    end_date = models.DateField()
    visible = models.BooleanField(default=False)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    sex = models.CharField(choices=SEX_CHOICES, max_length=2)
    number_of_appearing = models.PositiveIntegerField(default=0)
    number_of_pressing = models.PositiveIntegerField(default=0)
    number_of_appearing_days = models.PositiveIntegerField(default=0)
    accepted = models.BooleanField(default=False)


class AdsInformation(models.Model):
    gps = models.PositiveIntegerField()
    show_homepage = models.BooleanField(default=True)
    show_settings = models.BooleanField(default=True)
    show_profile = models.BooleanField(default=True)

class Discount(models.Model):
    manager_percentage = models.PositiveIntegerField()
    manager_days = models.PositiveIntegerField()
    supervisor_percentage = models.PositiveIntegerField()
    supervisor_days = models.PositiveIntegerField()

class AdvertisingPricing(models.Model):
    show_number_of_days = models.PositiveIntegerField()
    days_price = models.PositiveIntegerField()
    show_number_of_appearing = models.PositiveIntegerField()
    appearing_price = models.PositiveIntegerField()

class InactiveInformation(models.Model):
    unregistered_last_login = models.PositiveIntegerField()
    unregistered_last_view = models.PositiveIntegerField()
    registered_last_login = models.PositiveIntegerField()
    registered_last_view = models.PositiveIntegerField()
    certified_last_login = models.PositiveIntegerField()
    certified_last_view = models.PositiveIntegerField()

class AdsPromocode(models.Model):
    user = models.ForeignKey(AdminUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=40)
    ratio = models.CharField(max_length=10)
    entry_date = models.DateField(auto_now_add=True)
    valid_for = models.IntegerField(default=0)
    reason = models.TextField()