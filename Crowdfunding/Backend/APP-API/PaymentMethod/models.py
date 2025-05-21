import base64
from django.db import models
from django.conf import settings
from .utils import fernet
from datetime import date

class PaymentMethod(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payment_methods', null=True)
    holder_name = models.CharField(max_length=100)
    card_number = models.BinaryField()
    cvv = models.BinaryField()
    expiration_date = models.DateField(null=True, blank=True)

    def save_card(self, card_number, cvv):
        if isinstance(card_number, str):
            encrypted_card = fernet.encrypt(card_number.encode())
            self.card_number = base64.b64encode(encrypted_card)
        elif isinstance(card_number, bytes):
            self.card_number = card_number
        else:
            raise ValueError("card_number debe ser una cadena o bytes")

        if isinstance(cvv, str):
            encrypted_cvv = fernet.encrypt(cvv.encode())
            self.cvv = base64.b64encode(encrypted_cvv)
        elif isinstance(cvv, bytes):
            self.cvv = cvv
        else:
            raise ValueError("cvv debe ser una cadena o bytes")
    
    #  def save(self, *args, **kwargs):
    #      self.save_card(self.card_number, self.cvv)
    #      super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.payment_method_contributions.exists():
            self.user = None
            self.holder_name = ''
            self.cvv = fernet.encrypt(b'000')
            self.expiration_date = None
            self.save()
        else:
            super().delete(*args, **kwargs)

    def get_card_number(self):
        return fernet.decrypt(self.card_number).decode()
    
    def get_cvv(self):
        return fernet.decrypt(self.cvv).decode()
    
    def __str__(self):
        try:
            return f'**** **** **** {self.get_card_number()[-4:]} de {self.user}'
        except Exception:
            return 'Método de pago inválido'
    
    def is_expired(self):
        if not self.expiration_date:
            return True
        return self.expiration_date < date.today()
