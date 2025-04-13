from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Contribution
from .serializers import ContributionSerializer

class ContributionViewSet(viewsets.ModelViewSet):
    queryset = Contribution.objects.all()
    serializer_class = ContributionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        'project': ['exact'],
        'contributor': ['exact'],
        'payment_method': ['exact'],
        'date': ['date__gte', 'date__lte'],
    }
    ordering_fields = ['date', 'amount']
    search_fields = ['project__name', 'contributor__username']

    def perform_create(self, serializer):
        serializer.save(contributor=self.request.user)
