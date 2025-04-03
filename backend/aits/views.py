
from django.shortcuts import render
from rest_framework import serializers, viewsets,permissions,status, generics
from .models import Issue,Department,Notifications,Student,AcademicRegistrar,Lecturer
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import IssueSerializer,UserSerializer,DepartmentSerializer,NotificationsSerializer,LoginSerializer,StudentSerializer,StudentRegistrationSerializer,LecturerRegistrationSerializer,AcademicRegistrarSerializer,LecturerSerializer,LogoutSerializer,SignupSerializer
from django.contrib.auth import get_user_model
from .permissions import IsRegistrar,Isstudent, Islecturer
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.decorators import permission_classes, api_view, authentication_classes
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
    permission_classes = [AllowAny]
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

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        role = request.data.get('role')
        print("\n Registration Request")
        print('Recieved data:', request.data)

        if role == 'student':
            serializer = StudentRegistrationSerializer(data = request.data)
        elif role == 'lecturer':
            serializer = LecturerRegistrationSerializer(data = request.data)
        elif role == 'registrar':
            serializer == AcademicRegistrarSerializer(data = request.data)
        else:
            print('Invalid role')
            return Response(
                {'errors': {'role': f'Invalid role. Role must be: Student, Lecturer, Registrar'}},
                status=status.HTTP_400_BAD_REQUEST
            )
        if serializer.is_valid():
            try:
                instance = serializer.save
                user = instance.user
                print("User created successfully:", user.username)
                return Response({
                    'message': 'Registration successful',
                    'user': {
                        'userId': user.username,
                        'fullName': f"{user.first_name} {user.last_name}".strip(),
                        'email': user.email,
                        'role': user.role
                    }
                }, status=status.HTTP_201_CREATED)
            except serializers.ValidationError as e:
                print("Registration error:", str(e))
                return Response(
                    {'errors': {'general': 'Registration failed. Please try again.'}},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
def create_notification(recipient, notification_type, issue, message):
    """
    Helper function to create notifications
    """
    try:
        notification = Notifications.objects.create(
            recipient=recipient,
            notification_type=notification_type,
            issue=issue,
            message=message
        )
        print(f"Created notification: {notification.id} for user: {recipient.username}")
        return notification
    except Exception as e:
        print(f"Error creating notification: {str(e)}")
        return None

class StudentIssueCreateView(APIView):
    permission_classes = [IsAuthenticated, Isstudent]   
    def get(self, request):
        try:
            # Get the student instance
            student = request.user.student_profile
            
            # Get all issues for this student
            issues = Issue.objects.filter(student=student).order_by('-created_at')
            
            # Serialize the issues
            serializer = IssueSerializer(issues, many=True)
            
            return Response({
                'issues': serializer.data
            })
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            # Get the student instance
            student = request.user.student_profile
            
            # Create the issue
            serializer = IssueSerializer(data=request.data)
            if serializer.is_valid():
                # Add the student to the issue data
                serializer.validated_data['student'] = student
                
                # Save the issue
                issue = serializer.save()
                
                # Create notification for the student
                Notifications.objects.create(
                    recipient=request.user,
                    notification_type='issue_created',
                    issue=issue,
                    message=f'Your issue "{issue.title}" has been submitted successfully.'
                )
                
                return Response({
                    'message': 'Issue created successfully',
                    'issue': serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StudentIssueDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = IssueSerializer
    permission_classes = [Isstudent]

    def get_queryset(self):
        student = self.request.user.student_profile
        return Issue.objects.filter(student=student)

    def perform_update(self, serializer):
        student = self.request.user.student_profile
        issue = serializer.save(student=student)
        
        # Create notification for assigned lecturer if one is assigned
        if issue.assigned_to:
            create_notification(
                recipient=issue.assigned_to.user,
                notification_type='issue_updated',
                issue=issue,
                message=f'Issue updated: {issue.title}'
            )

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_issue(request, issue_id):
    try:
        issue = Issue.objects.get(pk=issue_id)
        old_status = issue.status
        old_assigned_to = issue.assigned_to

        # ... existing issue update code ...

        # Create notifications for status changes
        if old_status != issue.status:
            if issue.status == 'resolved':
                create_notification(
                    recipient=issue.student.user,
                    notification_type='issue_resolved',
                    issue=issue,
                    message=f'Your issue "{issue.title}" has been resolved'
                )

        # Create notifications for assignment changes
        if old_assigned_to != issue.assigned_to and issue.assigned_to:
            create_notification(
                recipient=issue.assigned_to.user,
                notification_type='issue_assigned',
                issue=issue,
                message=f'You have been assigned to issue: {issue.title}'
            )
        return False
    except Issue.DoesNotExist:
        return Response({'error': 'Issue not found'}, status=status.HTTP_404_NOT_FOUND)

class LecturerIssueListView(generics.ListAPIView):
    serializer_class = IssueSerializer
    permission_class = Islecturer

    def get_queryset(self):
        lecturer = self.request.user.lecturer_profile
        return Issue.objects.filter(lecturer=lecturer)

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