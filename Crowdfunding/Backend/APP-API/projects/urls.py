from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

app_name = 'projects'

router = DefaultRouter()
router.register(r'list', views.ProjectViewSet, basename='projects')
router.register(r'simple-project-list', views.SimpleProjectViewSet, basename='simple-projects')
router.register(r'categories', views.ProjectCategoryViewSet, basename='categories')
router.register(r'project-images', views.ProjectImageViewSet, basename='project-images')

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', views.ProjectStatsView.as_view(), name='project-stats'),
]