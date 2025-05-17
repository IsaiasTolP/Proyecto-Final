from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Project, ProjectCategory, ProjectImage
from .serializers import ProjectSerializer, ProjectCategorySerializer, ProjectImageSerializer, SimpleProjectSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response

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

class ProjectCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProjectCategory.objects.all()
    serializer_class = ProjectCategorySerializer

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