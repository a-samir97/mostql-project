from django.contrib import admin

from .models import AdsInformation, AdsPromocode, Advertising, AdvertisingPricing, InactiveInformation, Discount

admin.site.register(AdsInformation)
admin.site.register(AdsPromocode)
admin.site.register(Advertising)
admin.site.register(AdvertisingPricing)
admin.site.register(InactiveInformation)
admin.site.register(Discount)