from django.db import models
from django.conf import settings
from .utils import fernet
from datetime import date
from simple_history.models import HistoricalRecords


class PaymentMethod(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payment_methods', null=True)
    holder_name = models.CharField(max_length=100)
    card_number = models.BinaryField()
    cvv = models.BinaryField()
    expiration_date = models.DateField(null=True, blank=True)
    history = HistoricalRecords()

    def encrypt_if_needed(self, value):
        if isinstance(value, str):
            return fernet.encrypt(value.encode())
        elif isinstance(value, bytes):
            return value
        raise ValueError("Valor no válido para cifrado")

    def save(self, *args, **kwargs):
        self.card_number = self.encrypt_if_needed(self.card_number)
        self.cvv = self.encrypt_if_needed(self.cvv)
        super().save(*args, **kwargs)

    def get_card_number(self):
        return fernet.decrypt(self.card_number).decode()

    def get_cvv(self):
        return fernet.decrypt(self.cvv).decode()

    def delete(self, *args, **kwargs):
        if self.payment_method_contributions.exists():
            self.user = None
            self.holder_name = ''
            self.cvv = fernet.encrypt(b'000')
            self.expiration_date = None
            self.save()
        else:
            super().delete(*args, **kwargs)

    def __str__(self):
        try:
            return f'**** **** **** {self.get_card_number()[-4:]} de {self.user}'
        except Exception:
            return f'Método de pago inválido de {self.user}'

    def is_expired(self):
        if not self.expiration_date:
            return True
        return self.expiration_date < date.today()
