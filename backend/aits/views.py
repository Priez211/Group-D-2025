from django.shortcuts import render
from rest_framework import viewsets,permissions
from .models import Issue,Department,Notifications
from rest_framework.permissions import IsAuthenticated
from .serializers import IssueSerializer,UserSerializer,DepartmentSerializer,NotificationsSerializer
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .permissions import IsRegistrar,Islecturer,Isstudent,IsOwnerOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import LoginSerializer
from rest_framework.decorators import permission_classes, authentication_classes


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
        return super().get_permissions()
    def perform_create(self,serializer):
        # auto assigns issue to the logged in student
        if hasattr(self.request.user,'student'):
            serializer.save(student=self.request.user)
        else:
            raise permissions.PermissionDenied("Only students can create issues.")
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset=Department.objects.all()
    serializer_class=DepartmentSerializer
class NotificationsViewSet(viewsets.ModelViewSet):
    queryset=Notifications.objects.all()
    serializer_class=NotificationsSerializer
    permission_classes=[permissions.IsAuthenticated]
    def get_query(self):
        user=self.request.user
        return Notifications.objects.filter(user=user).order_by('-created_at')
class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid(): 
           return Response(serializer.validated_data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def protected_view(request):
        return Response({'message':"You are authenticated"})
    
    
    


    




