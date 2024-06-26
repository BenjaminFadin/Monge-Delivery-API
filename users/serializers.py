from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'telegram_id',
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'birth_date',
            'language'
        ]
        
