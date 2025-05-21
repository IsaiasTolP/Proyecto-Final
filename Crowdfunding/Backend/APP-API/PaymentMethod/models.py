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

    def save_card(self, card_number, cvv):
        if isinstance(card_number, str):
            self.card_number = fernet.encrypt(card_number.encode())
        elif isinstance(card_number, bytes):
            self.card_number = card_number

        if isinstance(cvv, str):
            self.cvv = fernet.encrypt(cvv.encode())
        elif isinstance(cvv, bytes):
            self.cvv = cvv
    
    def save(self, *args, **kwargs):
        if isinstance(self.card_number, str) or isinstance(self.cvv, str):
            self.save_card(self.card_number, self.cvv)
            super().save(*args, **kwargs)

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
        return f'**** **** **** {self.get_card_number()[-4:]} de {self.user}'
    
    def is_expired(self):
        if not self.expiration_date:
            return True
        return self.expiration_date < date.today()
