from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=250, blank=True)
    pfp = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class FounderProfile(Profile):
    website = models.URLField(max_length=200, blank=True)
    social_media = models.JSONField(blank=True, default=dict)  # Store social media links as JSON
    contact_email = models.EmailField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.user.username} Founder Profile'
