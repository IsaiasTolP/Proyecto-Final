from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Profile, FounderProfile
from .serializers import ProfileSerializer, FounderProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['location']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def get_user_profile(self, request, user_id=None):
        try:
            profile = Profile.objects.get(user__id=user_id)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get', 'put'], url_path='me', permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        profile = request.user.profile
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        
        if request.method == 'PUT':
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class FounderProfileViewSet(viewsets.ModelViewSet):
    queryset = FounderProfile.objects.all()
    serializer_class = FounderProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['location', 'contact_email', 'website', 'user']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def get_user_profile(self, request, user_id=None):
        try:
            profile = FounderProfile.objects.get(user__id=user_id)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except FounderProfile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get', 'put'], url_path='me', permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        try:
            founder_profile = FounderProfile.objects.get(user=request.user)
        except FounderProfile.DoesNotExist:
            return Response({"detail": "No founder profile found."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            serializer = self.get_serializer(founder_profile)
            return Response(serializer.data)
        
        if request.method == 'PUT':
            serializer = self.get_serializer(founder_profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
