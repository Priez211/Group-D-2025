from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from .models import Issue, Student, Lecturer, User, Notification
from .serializers import (
    IssueSerializer, 
    LoginSerializer,
    StudentRegistrationSerializer,
    LecturerRegistrationSerializer,
    NotificationSerializer,
    RegistrarRegistrationSerializer
)
from .permissions import IsStudent, IsLecturer, IsAcademicRegistrar
import jwt
import traceback
import datetime
from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            role = serializer.validated_data['role']
            # Get current timestamp and set expiration
            now = datetime.datetime.utcnow()
            exp = now + datetime.timedelta(hours=24)
            
                     

                    # Generate JWT token
            token = jwt.encode(
                        {'user_id': user.username, 'role': role,'exp':int(exp.timestamp())},
                        settings.SECRET_KEY,
                        algorithm='HS256'
                    )
                    
            return Response({
                        'token': token,
                        'user': {
                            'userId': user.username,
                            'fullName': f"{user.first_name} {user.last_name}".strip(),
                            'email': user.email,
                            'role': role
                        }
                    },status=status.HTTP_200_OK)
            
        return Response(
            {'error': serializer.errors.get('non_field_errors', ['Invalid credentials'])[0]},
            status=status.HTTP_401_UNAUTHORIZED)
        

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        role = request.data.get('role')
        print("\n=== Registration Request ===")
        print("Received data:", request.data)
        
        if role == 'student':
            serializer = StudentRegistrationSerializer(data=request.data)
        elif role == 'lecturer':
            serializer = LecturerRegistrationSerializer(data=request.data)
        elif role == 'registrar':
            serializer = RegistrarRegistrationSerializer(data=request.data)
        else:
            print("Invalid role:", role)
            return Response(
                {'errors': {'role': f'Invalid role. Must be one of: student, lecturer, registrar'}},
                status=status.HTTP_400_BAD_REQUEST
            )

        if serializer.is_valid():
            try:
                instance = serializer.save()
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
                print("Validation error:", str(e))
                return Response({'errors': {'general': str(e)}}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print("Registration error:", str(e))
                print("Traceback:", traceback.format_exc())
                return Response(
                    {'errors': {'general': 'Registration failed. Please try again.'}},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        # Format validation errors
        errors = {}
        for field, error_list in serializer.errors.items():
            errors[field] = error_list[0] if isinstance(error_list, list) else error_list
        
        print("Validation errors:", errors)
        return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

class StudentIssueCreateView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]
    
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
                Notification.objects.create(
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


class LecturerIssueListView(generics.ListAPIView):
    serializer_class = IssueSerializer
    permission_class = IsLecturer

    def get_queryset(self):
        lecturer = self.request.user.lecturer_profile
        return Issue.objects.filter(lecturer=lecturer)


class IssueUpdateView(generics.UpdateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsLecturer | IsAcademicRegistrar]


class StudentIssueDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = IssueSerializer
    permission_classes = [IsStudent]

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


class LecturerIssueDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = IssueSerializer
    permission_class = IsLecturer

    def get_queryset(self):
        lecturer = self.request.user.lecturer_profile
        return Issue.objects.filter(assigned_to=lecturer)

    def perform_update(self, serializer):
        lecturer = self.request.user.lecturer_profile
        issue = serializer.save()
        
        # Create notification for the student
        create_notification(
            recipient=issue.student.user,
            notification_type='issue_updated',
            issue=issue,
            message=f'Your issue "{issue.title}" has been updated by {lecturer.user.get_full_name()}'
        )
        
        # If the issue is marked as resolved, create a resolution notification
        if issue.status == 'resolved':
            create_notification(
                recipient=issue.student.user,
                notification_type='issue_resolved',
                issue=issue,
                message=f'Your issue "{issue.title}" has been resolved'
            )


class AcademicRegistrarIssueListView(generics.ListAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_class = IsAcademicRegistrar


class IssueDeleteView(generics.DestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_class = IsAcademicRegistrar


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    try:
        print(f"Fetching notifications for user: {request.user.username}")
        notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
        print(f"Found {notifications.count()} notifications")
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(f"Error in get_notifications: {str(e)}")
        return Response(
            {'error': 'Failed to fetch notifications', 'detail': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, recipient=request.user)
        notification.is_read = True
        notification.save()
        return Response({'status': 'success'})
    except Notification.DoesNotExist:
        return Response(
            {'error': 'Notification not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        print(f"Error in mark_notification_read: {str(e)}")
        return Response(
            {'error': 'Failed to mark notification as read', 'detail': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def create_notification(recipient, notification_type, issue, message):
    """
    Helper function to create notifications
    """
    try:
        notification = Notification.objects.create(
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_issue(request):
    try:
        # ... existing issue creation code ...

        # Create notification for assigned lecturer
        if issue.assigned_to:
            create_notification(
                recipient=issue.assigned_to.user,
                notification_type='issue_assigned',
                issue=issue,
                message=f'You have been assigned a new issue: {issue.title}'
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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

        return Response(serializer.data)
    except Issue.DoesNotExist:
        return Response({'error': 'Issue not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

