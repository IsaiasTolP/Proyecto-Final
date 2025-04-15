from django.contrib.auth.models import User
from rest_framework import serializers
from accounts.models import Profile, FounderProfile

class UserSerializer(serializers.ModelSerializer):
    is_founder = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'is_founder']
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        profile = Profile.objects.create(user=user, is_founder=validated_data['is_founder'])

        if profile.is_founder:
            FounderProfile.objects.create(user=user, profile=profile)

        return user
