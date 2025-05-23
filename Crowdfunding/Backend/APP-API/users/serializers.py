from django.contrib.auth.models import User
from rest_framework import serializers
from accounts.models import Profile, FounderProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    is_founder = serializers.BooleanField(default=False)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'is_founder']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        is_founder = validated_data.pop('is_founder')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        if not is_founder:
            Profile.objects.create(user=user, is_founder=is_founder)
        else:
            FounderProfile.objects.create(user=user, is_founder=is_founder)

        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        try:
            representation['is_founder'] = instance.profile.is_founder
        except Profile.DoesNotExist:
            representation['is_founder'] = False
        return representation

class SimpleUserSerializer(serializers.ModelSerializer):
    is_founder = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'is_founder']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        try:
            representation['is_founder'] = instance.profile.is_founder
        except Profile.DoesNotExist:
            representation['is_founder'] = False
        return representation

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        return super().get_token(user)
