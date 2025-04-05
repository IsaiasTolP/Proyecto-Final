from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=75)
    description = models.TextField()
    goal = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='project_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_images/')

    def __str__(self):
        return f'{self.project.name} - Image {self.id}'