from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import SmartResize
from django.db.models import Sum
from shared.utils import unique_project_image_upload_path
from colorfield.fields import ColorField
from PaymentMethod.models import PaymentMethod
from simple_history.models import HistoricalRecords


class ProjectCategory(models.Model):
    category = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=50, default='fa-solid fa-question')
    color = ColorField(default='#7c3aed')
    history = HistoricalRecords()


    def __str__(self):
        return self.category

class Project(models.Model):
    name = models.CharField(max_length=75)
    description = models.TextField()
    goal = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(ProjectCategory, related_name='category_projects', on_delete=models.PROTECT)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_projects', on_delete=models.CASCADE, null=True)
    featured = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.name
    
    @property
    def total_donated(self):
        total = self.project_contributions.aggregate(total=Sum('amount'))['total']
        return total or 0
    
    @property
    def percent_completed(self):
        if self.goal > 0:
            return round((float(self.total_donated) / float(self.goal)) * 100, 2)
        return 0
    
    @property
    def is_completed(self):
        return self.percent_completed >= 100

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='project_images', on_delete=models.CASCADE)
    image = ProcessedImageField(
        upload_to=unique_project_image_upload_path,
        processors=[SmartResize(900, 600)],
        format='JPEG',
        options={'quality': 90},
        default='project_images/default.jpg'
    )
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.project.name} - Image {self.id}'

class ProjectSponsorship(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sponsorships', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='sponsorships', on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    date = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.user} patrocinó {self.project} por {self.amount} €"
