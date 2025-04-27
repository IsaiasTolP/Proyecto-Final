from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Profile, FounderProfile
from .serializers import ProfileSerializer, FounderProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['location']

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def get_user_profile(self, request, user_id=None):
        try:
            profile = Profile.objects.get(user__id=user_id)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)


class FounderProfileViewSet(viewsets.ModelViewSet):
    queryset = FounderProfile.objects.all()
    serializer_class = FounderProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contact_email', 'website', 'user']
