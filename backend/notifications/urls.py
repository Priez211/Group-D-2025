from django.urls import path
from . import views

urlpatterns = [
    path('unread-count/', views.get_unread_count, name='notification-unread-count'),
] 