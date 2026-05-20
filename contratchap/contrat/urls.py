from django.urls import path
from .views import HttpResponse

urlpatterns = [
    path('register/', HttpResponse, name='register'),
]