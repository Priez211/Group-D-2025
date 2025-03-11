from django.shortcuts import render
from rest_framwork import viewsets,permisssions
from .models import Issue
from rest_framework.permissions import IsAuthenticated
from .serializers import IssueSerializer,UserSerializer
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .permissions import IsRegistrar,Islecturer,Isstudent
from rest_framework.authentication import TokenAuthentication

User=get_user_model()
class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes=[permissions.IsAuthenticated,IsRegistrar]#only registrars can manage the users

# Create your views here.
