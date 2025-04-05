from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=250, blank=True)
    pfp = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    location = models.CharField(max_length=100, blank=True)
