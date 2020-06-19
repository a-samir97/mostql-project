from rest_framework import serializers
from .models import AppUser, Accounts

class AccountsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Accounts
        exclude = ('id',)

# registered user 
# login via google, facebook 
class UserSerializer(serializers.ModelSerializer):

    accounts = AccountsSerializer()

    class Meta:
        model = AppUser
        fields = [
            'user_token', 'login_via','name_id', 
            'username', 'bio', 'email', 
            'receive_email', 'country',
            'state', 'sex', 'age', 'nickname',
            'visible_in_search', 'image', 'accounts']

    def create(self, validated_data):
        accounts = validated_data.pop('accounts')
        user_accounts = Accounts.objects.create(**accounts)
        user = AppUser.objects.create(**validated_data, accounts=user_accounts)

        return user

# unregistered user 
class UnregisteredUserSerializer(serializers.ModelSerializer):

    accounts = AccountsSerializer()

    class Meta:
        model = AppUser
        fields = [
            'name_id', 'username', 'bio',
            'email', 'receive_email', 'country',
            'state', 'sex', 'age', 'accounts'
        ]
    
    def create(self, validated_data):
        accounts = validated_data.pop('accounts')
        user_accounts = Accounts.objects.create(**accounts)
        user = AppUser.objects.create(**validated_data, accounts=user_accounts)

        return user

# user show 
class UserShowSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppUser
        fields = ['name_id', 'bio', 'image']