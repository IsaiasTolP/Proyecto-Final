from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Project, ProjectCategory, ProjectImage, ProjectSponsorship
from .serializers import ProjectSerializer, ProjectCategorySerializer, ProjectImageSerializer, SimpleProjectSerializer, ProjectSponsorshipSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from accounts.models import Profile
from django.db.models import Count

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_active', 'owner']
    ordering_fields = ['start_date', 'goal']
    search_fields = ['name']
    permission_classes = [AllowAny, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def latest(self, request):
        latest_projects = self.queryset.order_by('-start_date')[:3]
        serializer = self.get_serializer(latest_projects, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_projects = self.queryset.filter(featured=True)
        serializer = self.get_serializer(featured_projects, many=True)
        return Response(serializer.data)


class ProjectCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectCategorySerializer

    def get_queryset(self):
        return ProjectCategory.objects.annotate(num_projects=Count('category_projects'))

class ProjectImageViewSet(viewsets.ModelViewSet):
    queryset = ProjectImage.objects.all()
    serializer_class = ProjectImageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'project': ['exact'],
    }

class SimpleProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = SimpleProjectSerializer

class ProjectStatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        total_donated = sum(project.total_donated for project in Project.objects.all())
        total_projects = Project.objects.count()
        active_projects = Project.objects.filter(is_active=True).count()
        completed_projects = sum(project.is_completed for project in Project.objects.all())
        users = Profile.objects.count()

        return Response({
            'total_donated': total_donated,
            'total_projects': total_projects,
            'active_projects': active_projects,
            'completed_projects': completed_projects,
            'users': users
        })


class ProjectSponsorshipViewSet(viewsets.ModelViewSet):
    queryset = ProjectSponsorship.objects.all()
    serializer_class = ProjectSponsorshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
