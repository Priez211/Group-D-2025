from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,IssueViewSet


router=DefaultRouter()
router.register(r'users',UserViewSet)
router.register(r'issues',IssueViewSet)

urlpatterns=[
    path('',include(router.urls))
]