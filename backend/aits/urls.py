from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,IssueViewSet,DepartmentViewSet,NotificationsViewSet


router=DefaultRouter()
router.register(r'users',UserViewSet)
router.register(r'issues',IssueViewSet)
router.register(r'departments',DepartmentViewSet)
router.register(r'Notifications',NotificationsViewSet,basename='notifications')

urlpatterns=[
    path('',include(router.urls))
]