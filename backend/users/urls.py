from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_user, name='register'),
    # Add other user-related endpoints here
] 