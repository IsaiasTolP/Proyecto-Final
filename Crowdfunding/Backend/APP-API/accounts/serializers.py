from rest_framework import serializers
from .models import Profile, FounderProfile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['user']

class FounderProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FounderProfile
        fields = '__all__'
        read_only_fields = ['user']