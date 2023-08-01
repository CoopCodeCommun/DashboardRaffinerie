from rest_framework import serializers

from dashboard_user.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'uuid',
            'email',
        ]
        read_only_fields = ('uuid','email',)
