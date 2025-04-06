from django.db import models


class ProjectCategory(models.Model):
    category = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.category

class Project(models.Model):
    name = models.CharField(max_length=75)
    description = models.TextField()
    goal = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(ProjectCategory, related_name='projects', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='project_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_images/')

    def __str__(self):
        return f'{self.project.name} - Image {self.id}'
