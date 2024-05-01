from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'tg_user_id',
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'lang'
        ]
