from rest_framework import serializers
from users.models import AppUser
from users.serializers import AccountsSerializer
import datetime

class AppUserSerializer(serializers.ModelSerializer):
    accounts = AccountsSerializer()
    followers = serializers.SerializerMethodField('get_followers_number')
    class Meta:
        model = AppUser
        fields = [
            'name_id', 'username', 'bio',
            'login_via', 'sex', 'age',
            'country', 'last_login_date', 
            'ip_sign_in_today', 'last_view_date',
            'accounts', 'followers']
    
    def get_followers_number(self, obj):
        return obj.friends.all().count()

    
class ShowBlockedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['name_id', 'is_blocked', 'block_time']

class ShowInactiveUserSerializer(serializers.ModelSerializer):
    days_of_last_login = serializers.SerializerMethodField('get_login_days')
    days_of_last_visit = serializers.SerializerMethodField('get_visit_days')

    class Meta:
        model = AppUser
        fields = ['name_id', 'last_login_date', 
            'last_view_date', 'days_of_last_login', 'days_of_last_visit']
    
    def get_login_days(self, obj):
        return (datetime.datetime.now().date() - obj.last_login_date.date()).days
    
    def get_visit_days(self, obj):
        return (datetime.datetime.now().date() - obj.last_view_date.date()).days
