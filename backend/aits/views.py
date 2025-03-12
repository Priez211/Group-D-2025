from django.shortcuts import render
from rest_framework import viewsets,permissions
from .models import Issue,Department
from rest_framework.permissions import IsAuthenticated
from .serializers import IssueSerializer,UserSerializer,DepartmentSerializer
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .permissions import IsRegistrar,Islecturer,Isstudent,IsOwnerOrReadOnly
from rest_framework.authentication import TokenAuthentication
# Create your views here.
User=get_user_model()
class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes=[permissions.IsAuthenticated,IsRegistrar]#only registrars can manage the users
class IssueViewSet(viewsets.ModelViewSet):
    queryset=Issue.objects.all()
    serializer_class=IssueSerializer
    def get_permissions(self):
        if self.action in ['create']:
            return [Isstudent()]
        elif self.action in ['update','partial_update','destroy']:
            return [IsOwnerOrReadOnly()]
        elif self.action in ['list','retrieve']:
            return[permissions.IsAuthenticated()]
        return super().get_permissions
    def perform_create(self,serializer):
        serializer.save(student=self.request.user)# auto assigns issue to the logged in student
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset=Department.objects.all()
    Serializer_class=DepartmentSerializer
    




