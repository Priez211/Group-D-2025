
from django.shortcuts import render
from rest_framework import serializers, viewsets,permissions,status
from .models import Issue,Department,Notifications,Student,AcademicRegistrar,Lecturer
from rest_framework.permissions import IsAuthenticated
from .serializers import IssueSerializer,UserSerializer,DepartmentSerializer,NotificationsSerializer,LoginSerializer,StudentSerializer,AcademicRegistrarSerializer,LecturerSerializer,LogoutSerializer,SignupSerializer
from django.contrib.auth import get_user_model
from .permissions import IsRegistrar,Isstudent
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
User=get_user_model()
class SignupView(APIView):
    def post(self,request):
        serializer=SignupSerializer(data=request.data)
        if serializer.is_valid():
            User=serializer.save()
            return Response({
                "message":"User registered successfully","user":serializer.data},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid(): 
           username=serializer.validated_data['username']
           password=serializer.validated_data['password']
           User=authenticate(username=username,password=password)
           if User:
               refresh=RefreshToken.for_user(User)
               #Determines the user role
               role="Unknown"
               if hasattr(User,'student'):
                   role="Student"
               elif hasattr(User,'registrar'):
                   role="Academic Registrar"
               elif hasattr(User,'lecturer'):
                   role="Lecturer"
               return Response({
                   'refresh':str(refresh),
                   'access':str(refresh.access_token),
                   'role':role,
                   'user_id':User.id,
                   'username':User.username
               },status=status.HTTP_200_OK)
           return Response({"error":"Invalid credentials"},status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def protected_view(request):
        return Response({'message':"You are authenticated"})
    

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
class StudentViewSet(viewsets.ModelViewSet):
    queryset=Student.objects.all()
    serializer_class=StudentSerializer
    permission_classes=[permissions.IsAuthenticated]
    
class AcademicRegistrarViewSet(viewsets.ModelViewSet):
    queryset=AcademicRegistrar.objects.all()
    serializer_class=AcademicRegistrarSerializer
    permission_classes=[permissions.IsAuthenticated]

class LecturerViewSet(viewsets.ModelViewSet):
    queryset=Lecturer.objects.all()
    serializer_class=LecturerSerializer
    permission_classes=[permissions.IsAuthenticated]
class LogoutView(APIView):
    
    ##Handles user logout by blacklisting the refresh token.
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request):
        serializer=LogoutSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message":"Logged out successfully"},status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


