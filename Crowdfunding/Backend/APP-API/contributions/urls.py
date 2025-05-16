from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

app_name = 'contributions'

router = DefaultRouter()
router.register(r'list', views.ContributionViewSet, basename='contribution')
router.register(r'simple', views.SimpleContributionViewSet, basename='simple-contribution')

urlpatterns = [
    path('', include(router.urls)),
]

