# serializers.py
from rest_framework import serializers
from .models import PaymentMethod

class PaymentMethodSerializer(serializers.ModelSerializer):
    card_last4  = serializers.SerializerMethodField(read_only=True)
    card_number = serializers.CharField(write_only=True, max_length=19)
    cvv         = serializers.CharField(write_only=True, max_length=4)

    class Meta:
        model  = PaymentMethod
        fields = [
            'id',
            'holder_name',
            'expiration_date',
            'card_number',
            'cvv',
            'card_last4',
        ]

    def get_card_last4(self, obj):
        try:
            return obj.get_card_number()[-4:]
        except Exception:
            return "****"

    def create(self, validated_data):
        card = validated_data.pop('card_number')
        cvv  = validated_data.pop('cvv')
        validated_data['card_number'] = PaymentMethod.encrypt_text(card)
        validated_data['cvv']         = PaymentMethod.encrypt_text(cvv)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'card_number' in validated_data:
            instance.card_number = PaymentMethod.encrypt_text(validated_data.pop('card_number'))
        if 'cvv' in validated_data:
            instance.cvv = PaymentMethod.encrypt_text(validated_data.pop('cvv'))

        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        return instance
