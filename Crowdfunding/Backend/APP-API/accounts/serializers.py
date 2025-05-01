from rest_framework import serializers
from PIL import Image
from .models import Profile, FounderProfile
from users.serializers import UserSerializer

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'pfp', 'location', 'is_founder' ]

    def validate_pfp(self, value):
        try:
            image = Image.open(value)
            if image.format.lower() not in ['jpeg', 'jpg', 'png']:
                raise serializers.ValidationError('Solo se permiten imágenes en formato JPG o PNG.')
        except Exception:
            raise serializers.ValidationError('Archivo de imagen inválido.')
        return value


class FounderProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = FounderProfile
        fields = ['id', 'user', 'bio', 'pfp', 'location', 'is_founder', 'website', 'social_media', 'contact_email']
    
    def validate_pfp(self, value):
        try:
            image = Image.open(value)
            if image.format.lower() not in ['jpeg', 'jpg', 'png']:
                raise serializers.ValidationError('Solo se permiten imágenes en formato JPG o PNG.')
        except Exception:
            raise serializers.ValidationError('Archivo de imagen inválido.')
        return value
