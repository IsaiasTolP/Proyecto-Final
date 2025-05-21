from django.db import models
from django.conf import settings
from .utils import fernet
from datetime import date

class PaymentMethod(models.Model):
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='payment_methods',
    null=True)
    holder_name = models.CharField(max_length=100)
    card_number = models.BinaryField()
    cvv = models.BinaryField()
    expiration_date = models.DateField(null=True, blank=True)

    @staticmethod
    def encrypt_text(text: str) -> bytes:
        return fernet.encrypt(text.encode())

    def get_card_number(self) -> str:
        return fernet.decrypt(self.card_number).decode()

    def get_cvv(self) -> str:
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

    def is_expired(self) -> bool:
        return not self.expiration_date or self.expiration_date < date.today()

