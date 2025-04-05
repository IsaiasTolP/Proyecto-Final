from django.db import models
from projects.models import Project
from django.conf import settings

class Contribution(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, related_name='project_contributions', on_delete=models.PROTECT)
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_contributions', on_delete=models.PROTECT)

