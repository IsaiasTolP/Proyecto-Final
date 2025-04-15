from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, FounderProfileViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'founders', FounderProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
