# users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView  # Importamos la vista para refrescar el token
from .views import RegisterUserAPIView, UserMeView, UserDetailView, CustomLoginView

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name='register_user'),
    path('login/', CustomLoginView.as_view(), name='login_user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Endpoint para refrescar el token
    path('<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('me/', UserMeView.as_view(), name='user_me')
]
