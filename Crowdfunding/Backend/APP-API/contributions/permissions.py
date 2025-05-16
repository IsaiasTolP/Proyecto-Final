from rest_framework.permissions import BasePermission
from .models import Contribution

class IsOwnerOrNotAllowed(BasePermission):

    def has_object_permission(self, request, view, obj: Contribution):
        return request.user.id == obj.contributor.id