from rest_framework import serializers

from .models import AdsPromocode, Advertising

from datetime import timedelta

class PromocodeSerializer(serializers.ModelSerializer):
    end_date = serializers.SerializerMethodField('get_end_date')
    class Meta:
        model = AdsPromocode
        fields = '__all__'
    
    def get_end_date(self, obj):
        return obj.entry_date + timedelta(days=obj.valid_for)

class AdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertising
        fields = "__all__"