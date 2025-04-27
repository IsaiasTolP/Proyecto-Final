from rest_framework import serializers
from .models import Profile, FounderProfile
from users.serializers import UserSerializer

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'pfp', 'location', 'is_founder' ]

class FounderProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = FounderProfile
        fields = '__all__'