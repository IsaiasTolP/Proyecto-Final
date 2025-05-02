from rest_framework import serializers
from .models import PaymentMethod

class PaymentMethodSerializer(serializers.ModelSerializer):
    card_last4 = serializers.SerializerMethodField()

    class Meta:
        model = PaymentMethod
        fields = ['id', 'holder_name', 'expiration_date', 'card_last4']

    def get_card_last4(self, obj):
        try:
            return obj.get_card_number()[-4:]
        except Exception:
            return "****"
