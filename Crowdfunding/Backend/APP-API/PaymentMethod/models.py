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
            self.card_number = fernet.encrypt(card_number.encode())
        elif isinstance(card_number, bytes):
            self.card_number = card_number
        else:
            raise ValueError("card_number debe ser una cadena o bytes")

        if isinstance(cvv, str):
            self.cvv = fernet.encrypt(cvv.encode())
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
        try:
            encrypted_data = bytes(self.card_number) if not isinstance(self.card_number, bytes) else self.card_number
            return fernet.decrypt(encrypted_data).decode()
        except Exception as e:
            print(f"Error desencriptando card_number: {e}")
            return "****"

    def get_cvv(self):
        try:
            encrypted_data = bytes(self.cvv) if not isinstance(self.cvv, bytes) else self.cvv
            return fernet.decrypt(encrypted_data).decode()
        except Exception as e:
            print(f"Error desencriptando cvv: {e}")
            return "***"
    
    def __str__(self):
        try:
            return f'**** **** **** {self.get_card_number()[-4:]} de {self.user}'
        except Exception:
            return 'Método de pago inválido'
    
    def is_expired(self):
        if not self.expiration_date:
            return True
        return self.expiration_date < date.today()
