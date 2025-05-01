from django.contrib.auth.models import User
from rest_framework import serializers
from accounts.models import Profile, FounderProfile

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
        user.set_password(password) # Assures the password is hashed
        user.save()

        if not is_founder:
            Profile.objects.create(user=user, is_founder=is_founder)
        else:
            FounderProfile.objects.create(user=user, is_founder=is_founder)

        return user
    
    def get_is_founder(self, instance):
        representation = super().to_representation(instance)
        try:
            representation['is_founder'] = instance.profile.is_founder
        except Profile.DoesNotExist:
            representation['is_founder'] = False
        return representation
