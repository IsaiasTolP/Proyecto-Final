from django.db import models
from projects.models import Project
from django.conf import settings
from PaymentMethod.models import PaymentMethod

class Contribution(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    message = models.CharField(blank=True, max_length=140)
    project = models.ForeignKey(Project, related_name='project_contributions', on_delete=models.PROTECT)
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_contributions', on_delete=models.PROTECT)
    payment_method = models.ForeignKey(PaymentMethod, related_name='payment_method_contributions', on_delete=models.PROTECT)

    def __str__(self):
        return f'Contribution of {self.amount} to {self.project.name} by {self.contributor.username}'
