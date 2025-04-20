from django.contrib.auth.models import User
from rest_framework import serializers
from accounts.models import Profile, FounderProfile

class UserSerializer(serializers.ModelSerializer):
    is_founder = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'is_founder']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        is_founder = validated_data.pop('is_founder')
        user = User.objects.create_user(**validated_data)

        if not is_founder:
            Profile.objects.create(user=user, is_founder=is_founder)
        else:
            FounderProfile.objects.create(user=user, is_founder=is_founder)

        return user
