from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Project, ProjectCategory, ProjectImage
from .serializers import ProjectSerializer, ProjectCategorySerializer, ProjectImageSerializer, SimpleProjectSerializer
from .permissions import IsOwnerOrReadOnly

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_active']
    ordering_fields = ['start_date', 'goal']
    search_fields = ['name']
    permission_classes = [AllowAny, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ProjectCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProjectCategory.objects.all()
    serializer_class = ProjectCategorySerializer

class ProjectImageViewSet(viewsets.ModelViewSet):
    queryset = ProjectImage.objects.all()
    serializer_class = ProjectImageSerializer

class SimpleProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = SimpleProjectSerializer