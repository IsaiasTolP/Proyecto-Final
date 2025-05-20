from rest_framework import serializers
from .models import Contribution
from users.serializers import UserSerializer, SimpleUserSerializer
from PaymentMethod.models import PaymentMethod
from projects.models import Project

class ContributionSerializer(serializers.ModelSerializer):
    contributor = UserSerializer(read_only=True)
    cvv = serializers.CharField(write_only=True, max_length=4, min_length=3)

    class Meta:
        model = Contribution
        fields = '__all__'
        read_only_fields = ['date']

    def validate_payment_method(self, value: PaymentMethod):
        request = self.context.get('request')
        user = request.user if request else None

        if value.is_expired():
            raise serializers.ValidationError("Payment method is expired.")

        if value.user != user:
            raise serializers.ValidationError("This payment method does not belong to you.")

        return value
    
    def validate_project(self, value: Project):
        if not value.is_active:
            raise serializers.ValidationError("Project is already closed.")
        return value
    
    def validate(self, data):
        payment_method = data.get('payment_method')
        input_cvv = data.pop('cvv', None)

        if not payment_method or not input_cvv:
            raise serializers.ValidationError('CVV is required')

        try:
            stored_cvv = payment_method.get_cvv()
        except Exception:
            raise serializers.ValidationError("Error verificating CVV number.")

        if str(stored_cvv) != str(input_cvv):
            raise serializers.ValidationError("CVV does not match the selected payment method.")

        return data


class SimpleContributionSerializer(serializers.ModelSerializer):
    contributor = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Contribution
        fields = ['id', 'amount', 'date', 'message', 'project', 'contributor']
        read_only_fields = fields