from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from shared.utils import unique_image_upload_path
from simple_history.models import HistoricalRecords

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=250, blank=True)
    pfp = ProcessedImageField(
        upload_to=unique_image_upload_path,
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 90},
        default='profile_pics/default.jpg')
    location = models.CharField(max_length=100, blank=True)
    is_founder = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.user.username} Profile'

class FounderProfile(Profile):
    website = models.URLField(max_length=200, blank=True)
    social_media = models.JSONField(blank=True, default=dict)  # Store social media links as JSON, name as key, url as value
    contact_email = models.EmailField(max_length=100, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.user.username} Founder Profile'
