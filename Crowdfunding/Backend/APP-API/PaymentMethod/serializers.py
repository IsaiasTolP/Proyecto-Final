from rest_framework import serializers
from .models import PaymentMethod

class PaymentMethodSerializer(serializers.ModelSerializer):
    card_last4 = serializers.SerializerMethodField(read_only=True)
    card_number = serializers.CharField(write_only=True, allow_blank=False, max_length=19)
    cvv = serializers.CharField(write_only=True, allow_blank=False, max_length=4)
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
        card_number = validated_data.pop('card_number', '')
        cvv = validated_data.pop('cvv', '')
        
        # Validación adicional
        if not isinstance(card_number, str) or not isinstance(cvv, str):
            raise serializers.ValidationError("card_number y cvv deben ser strings.")
        
        pm = PaymentMethod(**validated_data)
        pm.save_card(card_number, cvv)
        pm.save()
        return pm
    
    def update(self, instance: PaymentMethod, validated_data):
        card_number = validated_data.pop('card_number', None)
        cvv = validated_data.pop('cvv', None)
        
        if card_number is not None and not isinstance(card_number, str):
            raise serializers.ValidationError("card_number debe ser una cadena.")
        if cvv is not None and not isinstance(cvv, str):
            raise serializers.ValidationError("cvv debe ser una cadena.")
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if card_number is not None or cvv is not None:
            instance.save_card(
                card_number if card_number is not None else instance.card_number,
                cvv if cvv is not None else instance.cvv
            )
        
        instance.save()
        return instance
