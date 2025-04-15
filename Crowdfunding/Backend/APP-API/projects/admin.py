from django.contrib import admin
from .models import Project, ProjectCategory, ProjectImage

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    pass

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    pass
