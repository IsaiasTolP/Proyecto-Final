from rest_framework import serializers
from .models import PaymentMethod

class PaymentMethodSerializer(serializers.ModelSerializer):
    card_last4 = serializers.SerializerMethodField(read_only=True)
    card_number = serializers.CharField(write_only=True, allow_blank=True, max_length=19)
    cvv = serializers.CharField(write_only=True, allow_blank=True, max_length=4)
    class Meta:
        model = PaymentMethod
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
        card_number = validated_data.pop('card_number')
        cvv = validated_data.pop('cvv')
        pm = PaymentMethod(**validated_data)
        pm.save(card_number, cvv)
        return pm
    
    def update(self, instance: PaymentMethod, validated_data):
        card_number = validated_data.pop('card_number', None)
        cvv = validated_data.pop('cvv', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if card_number or cvv:
            instance.save(card_number or instance.card_number, cvv or instance.cvv)
        instance.save()
        return instance
