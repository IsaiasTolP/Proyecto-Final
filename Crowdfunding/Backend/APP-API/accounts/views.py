from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Profile, FounderProfile
from .serializers import ProfileSerializer, FounderProfileSerializer
from rest_framework.views import APIView
from projects.models import Project
from contributions.models import Contribution
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


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


class ProfileStatsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        user_id = request.query_params.get('user_id')

        if not user_id:
            return Response({'error': 'user_id is required'}, status=400)
        
        user = get_object_or_404(User, id=user_id)

        created_projects = Project.objects.filter(owner=user).count()
        supported_projects = Contribution.objects.filter(contributor=user).distinct().count()
        given_funds = sum(contribution.amount for contribution in Contribution.objects.filter(contributor=user))

        return Response({
            'created_projects': created_projects,
            'supported_projects': supported_projects,
            'given_funds': given_funds
        })