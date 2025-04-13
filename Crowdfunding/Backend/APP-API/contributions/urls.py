from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

app_name = 'contributions'

router = DefaultRouter()
router.register(r'contributions', views.ContributionViewSet)

url_patterns = [
    path('', include(router.urls)),
]

