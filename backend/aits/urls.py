from django.urls import path
from .views import (
    LoginView, 
    RegisterView, 
    StudentIssueCreateView,
    StudentIssueDetailView
)
from . import views

urlpatterns = [
    # URLs without trailing slash
    path('login', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('student/issues', StudentIssueCreateView.as_view(), name='student-issues'),
    path('student/issues/<int:pk>', StudentIssueDetailView.as_view(), name='student-issue-detail'),
    path('notifications', views.get_notifications, name='notifications'),
    path('notifications/<int:notification_id>/mark-read', views.mark_notification_read, name='mark-notification-read'),
    
    # URLs with trailing slash (Django's default)
    path('login/', LoginView.as_view(), name='login-slash'),
    path('register/', RegisterView.as_view(), name='register-slash'),
    path('student/issues/', StudentIssueCreateView.as_view(), name='student-issues-slash'),
    path('student/issues/<int:pk>/', StudentIssueDetailView.as_view(), name='student-issue-detail-slash'),
    path('notifications/', views.get_notifications, name='notifications-slash'),
    path('notifications/<int:notification_id>/mark-read/', views.mark_notification_read, name='mark-notification-read-slash'),
] 