from rest_framework import serializers
from .models import Contribution
from users.serializers import UserSerializer

class ContributionSerializer(serializers.ModelSerializer):
    contributor = UserSerializer(read_only=True)

    class Meta:
        model = Contribution
        fields = '__all__'
        read_only_fields = ['date']