from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

app_name = 'projects'

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet)
router.register(r'categories', views.ProjectCategoryViewSet)
router.register(r'project-images', views.ProjectImageViewSet)

url_patterns = [
    path('', include(router.urls)),
]