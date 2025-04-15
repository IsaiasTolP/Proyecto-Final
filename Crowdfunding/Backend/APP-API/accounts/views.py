from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Profile, FounderProfile
from .serializers import ProfileSerializer, FounderProfileSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['location', 'user']


class FounderProfileViewSet(viewsets.ModelViewSet):
    queryset = FounderProfile.objects.all()
    serializer_class = FounderProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contact_email', 'website', 'user']
