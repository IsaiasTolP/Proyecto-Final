from django.db import models
from django.conf import settings
from .utils import load_key

fernet = load_key()

class PaymentMethod(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payment_methods', null=True)
    holder_name = models.CharField(max_length=100)
    card_number = models.BinaryField()
    cvv = models.BinaryField()
    expiration_date = models.DateField()

    def save_card(self, card_number, cvv):
        self.card_number = fernet.encrypt(card_number.encode())
        self.cvv = fernet.encrypt(cvv.encode())

    def get_card_number(self):
        return fernet.decrypt(self.card_number).decode()
    
    def get_cvv(self):
        return fernet.decrypt(self.cvv).decode()
    
    def __str__(self):
        return f'**** **** **** {self.get_card_number()[-4:]}'
