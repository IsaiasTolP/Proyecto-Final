# admin.py
from django.contrib import admin
from django import forms
from .models import PaymentMethod
from .utils import fernet

class PaymentMethodAdminForm(forms.ModelForm):
    card_number_plain = forms.CharField(max_length=16, required=True, help_text="Número de tarjeta")
    cvv_plain = forms.CharField(max_length=4, required=True, help_text="Código de seguridad")

    class Meta:
        model = PaymentMethod
        exclude = ('card_number', 'cvv')  # Ocultamos los campos binarios

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.card_number = fernet.encrypt(self.cleaned_data['card_number_plain'].encode())
        instance.cvv = fernet.encrypt(self.cleaned_data['cvv_plain'].encode())
        if commit:
            instance.save()
        return instance

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    form = PaymentMethodAdminForm

    readonly_fields = ['masked_card']
    fieldsets = (
        (None, {
            'fields': ('user', 'holder_name', 'card_number_plain', 'cvv_plain', 'expiration_date', 'masked_card')
        }),
    )

    def masked_card(self, obj):
        try:
            return f'**** **** **** {obj.get_card_number()[-4:]}'
        except:
            return '[Error o tarjeta vacía]'
    masked_card.short_description = 'Número (últimos 4)'
