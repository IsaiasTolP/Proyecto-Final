from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.db.models import Sum


class ProjectCategory(models.Model):
    category = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.category

class Project(models.Model):
    name = models.CharField(max_length=75)
    description = models.TextField()
    goal = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(ProjectCategory, related_name='category_projects', on_delete=models.PROTECT)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_projects', on_delete=models.CASCADE)

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

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='project_images', on_delete=models.CASCADE)
    image = ProcessedImageField(
        upload_to='project_images/',
        processors=[ResizeToFill(800, 600)],
        format='JPEG',
        options={'quality': 90},
    )

    def __str__(self):
        return f'{self.project.name} - Image {self.id}'
