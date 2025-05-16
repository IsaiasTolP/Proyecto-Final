from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Contribution
from .serializers import ContributionSerializer, SimpleContributionSerializer
from .tasks import send_receipt_email, send_received_contribution_email
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrNotAllowed

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
    permission_classes = [IsAuthenticated, IsOwnerOrNotAllowed]

    def get_queryset(self):
        user = self.request.user
        return Contribution.objects.filter(contributor=user)

    def perform_create(self, serializer):
        contribution = serializer.save(contributor=self.request.user)

        send_receipt_email.delay(
            user_email=self.request.user.email,
            user_name=self.request.user.username,
            project_name=contribution.project.name,
            amount=contribution.amount
        )

        send_received_contribution_email.delay(
            user_email=contribution.project.owner.email,
            project_name=contribution.project.name,
            amount=contribution.amount
        )


class SimpleContributionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Contribution.objects.all()
    serializer_class = SimpleContributionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        'project': ['exact'],
        'contributor': ['exact'],
        'date': ['date__gte', 'date__lte'],
    }
    ordering_fields = ['date', 'amount']
    search_fields = ['project__name', 'contributor__username']
    permission_classes = [IsAuthenticated]