from django.urls import path
from .views import (
    RegisterView, 
    LoginView, 
    LogoutView,
    CSRFTokenView,
    UserProfileView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenVerifyView,
    TokenRefreshView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name="login-view"),
    path('logout/', LogoutView.as_view(), name='login-view'),

    # Jwt endpoints
    path('token', TokenObtainPairView.as_view(), name='Token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='Refresh_token'),
    path('token/verify', TokenVerifyView.as_view(), name='Token_verify'),

    # My profile
    path('me/', UserProfileView.as_view(), name='profile'),

    # Csrf
    path('csrf/', CSRFTokenView.as_view(), name='api-csrf'),
]