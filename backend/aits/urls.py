from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,IssueViewSet,DepartmentViewSet,NotificationsViewSet,LoginView,StudentViewSet,AcademicRegistrarViewSet,LecturerViewSet


router=DefaultRouter()
router.register(r'departments',DepartmentViewSet)
router.register(r'users',UserViewSet)
router.register(r'issues',IssueViewSet)
router.register(r'Notifications',NotificationsViewSet,basename='notifications')
router.register(r'students',StudentViewSet)
router.register(r'lecturers',LecturerViewSet)
router.register(r'registrars',AcademicRegistrarViewSet)

urlpatterns=[
    path('',include(router.urls)),
    path('api/Login/',LoginView.as_view(),name='Login'),
]
