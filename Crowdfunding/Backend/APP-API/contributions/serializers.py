from rest_framework import serializers
from .models import Contribution
from users.serializers import UserSerializer, SimpleUserSerializer
from PaymentMethod.models import PaymentMethod
from projects.models import Project

class ContributionSerializer(serializers.ModelSerializer):
    contributor = UserSerializer(read_only=True)

    class Meta:
        model = Contribution
        fields = '__all__'
        read_only_fields = ['date']

    def validate_payment_method(self, value: PaymentMethod):
        if value.is_expired():
            raise serializers.ValidationError("Payment method is expired.")
        return value
    
    def validate_project(self, value: Project):
        if not value.is_active:
            raise serializers.ValidationError("Project is already closed.")
        return value


class SimpleContributionSerializer(serializers.ModelSerializer):
    contributor = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Contribution
        fields = ['id', 'amount', 'date', 'message', 'project', 'contributor']
        read_only_fields = fields