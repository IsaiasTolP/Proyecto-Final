from rest_framework import serializers
from .models import Contribution

class ContributionSerializer(serializers.ModelSerializer):
    contributor = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Contribution
        fields = '__all__'
        read_only_fields = ['date']