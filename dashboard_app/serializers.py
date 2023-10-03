from rest_framework import serializers

from dashboard_user.models import CustomUser
from dashboard_app.models import AccountAccount


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'uuid',
            'email',
        ]
        read_only_fields = ('uuid','email',)


class AccountAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountAccount
        fields = '__all__'
