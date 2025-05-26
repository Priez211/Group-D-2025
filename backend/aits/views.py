from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from django.conf import settings
import jwt
import traceback
import datetime
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import Issue, Student, Lecturer, User, Notification
from .serializers import (
    IssueSerializer, 
    LoginSerializer,
    StudentRegistrationSerializer,
    LecturerRegistrationSerializer,
    NotificationSerializer,
    RegistrarRegistrationSerializer,
    StudentSerializer,
    LecturerSerializer
)
from .permissions import IsStudent, IsLecturer, IsAcademicRegistrar


class LoginView(APIView):
    """Handle user login and return JWT token"""
    permission_classes = [AllowAny]

    def post(self, request):
        # Check if login data is valid
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            role = serializer.validated_data['role']
            
            # Create JWT token that expires in 24 hours
            now = datetime.datetime.utcnow()
            exp = now + datetime.timedelta(hours=24)
            token = jwt.encode(
                {
                    'user_id': user.username,
                    'role': role,
                    'exp': int(exp.timestamp())
                },
                settings.SECRET_KEY,
                algorithm='HS256'
            )
            
            # Return token and user info
            return Response({
                'token': token,
                'user': {
                    'userId': user.username,
                    'fullName': f"{user.first_name} {user.last_name}".strip(),
                    'email': user.email,
                    'role': role
                }
            }, status=status.HTTP_200_OK)
            
        return Response(
            {'error': serializer.errors.get('non_field_errors', ['Invalid credentials'])[0]},
            status=status.HTTP_401_UNAUTHORIZED
        )


class RegisterView(APIView):
    """Handle user registration for different roles"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Get user role from request
        role = request.data.get('role')
        print("\n=== Registration Request ===")
        print("Received data:", request.data)
        
        # Choose serializer based on role
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

        # Try to create new user
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
        
        # Return validation errors if any
        errors = {}
        for field, error_list in serializer.errors.items():
            errors[field] = error_list[0] if isinstance(error_list, list) else error_list
        
        print("Validation errors:", errors)
        return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)


class StudentIssueCreateView(APIView):
    """Handle creating and listing student issues"""
    permission_classes = [IsAuthenticated, IsStudent]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    def get(self, request):
        try:
            # Get student's issues
            student = request.user.student_profile
            issues = Issue.objects.filter(student=student).order_by('-created_at')
            serializer = IssueSerializer(issues, many=True)
            return Response({'issues': serializer.data})
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            print("\n=== Creating New Issue ===")
            print(f"Request data: {request.data}")
            
            # Get student info
            student = request.user.student_profile
            print(f"Student: {student}")
            
            # Check if issue should be assigned to a lecturer
            assigned_to = None
            if 'assigned_to' in request.data:
                try:
                    assigned_to = Lecturer.objects.get(id=request.data['assigned_to'])
                    print(f"Assigning to lecturer: {assigned_to}")
                except Lecturer.DoesNotExist:
                    print(f"Lecturer with ID {request.data['assigned_to']} not found")
                    return Response({
                        'error': 'Selected lecturer does not exist'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create new issue
            serializer = IssueSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                print(f"Serializer is valid. Data: {serializer.validated_data}")
                
                # Add student and lecturer info
                serializer.validated_data['student'] = student
                if assigned_to:
                    serializer.validated_data['assigned_to'] = assigned_to
                
                # Handle file upload if any
                if 'attachment' in request.FILES:
                    serializer.validated_data['attachment'] = request.FILES['attachment']
                
                # Save issue
                issue = serializer.save()
                print(f"Issue created successfully: {issue}")
                
                # Send notification to student
                create_notification(
                    recipient=request.user,
                    notification_type='issue_created',
                    issue=issue,
                    message=f'Your issue "{issue.title}" has been submitted successfully.'
                )
                
                # Send notification to lecturer if assigned
                if assigned_to:
                    create_notification(
                        recipient=assigned_to.user,
                        notification_type='issue_assigned',
                        issue=issue,
                        message=f'You have been assigned a new issue: {issue.title}'
                    )
                    print(f"Notification sent to lecturer: {assigned_to}")
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            print(f"Error creating issue: {str(e)}")
            print("Traceback:", traceback.format_exc())
            return Response({
                'error': 'Failed to create issue. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LecturerIssueListView(generics.ListAPIView):
    """Get list of issues assigned to a lecturer"""
    serializer_class = IssueSerializer
    permission_classes = [IsLecturer]
    
    def get_queryset(self):
        return Issue.objects.filter(assigned_to=self.request.user.lecturer_profile)


class IssueUpdateView(generics.UpdateAPIView):
    """Update an existing issue"""
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        # Check if user has permission to update this issue
        if self.request.user.role == 'student':
            return [IsStudent()]
        elif self.request.user.role == 'lecturer':
            return [IsLecturer()]
        return [IsAuthenticated()]
    
    def perform_update(self, serializer):
        issue = serializer.save()
        
        # Send notification about update
        if issue.status == 'resolved':
            create_notification(
                recipient=issue.student.user,
                notification_type='issue_resolved',
                issue=issue,
                message=f'Your issue "{issue.title}" has been resolved.'
            )


class StudentIssueDetailView(generics.RetrieveUpdateAPIView):
    """View and update student's issue details"""
    serializer_class = IssueSerializer
    permission_classes = [IsStudent]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    def get_queryset(self):
        return Issue.objects.filter(student=self.request.user.student_profile)
    
    def perform_update(self, serializer):
        issue = serializer.save()
        
        # Send notification if issue is updated
        create_notification(
            recipient=self.request.user,
            notification_type='issue_updated',
            issue=issue,
            message=f'Your issue "{issue.title}" has been updated.'
        )
        
        # Notify lecturer if assigned
        if issue.assigned_to:
            create_notification(
                recipient=issue.assigned_to.user,
                notification_type='issue_updated',
                issue=issue,
                message=f'Issue "{issue.title}" has been updated by the student.'
            )


class LecturerIssueDetailView(generics.RetrieveUpdateAPIView):
    """View and update lecturer's assigned issue details"""
    serializer_class = IssueSerializer
    permission_classes = [IsLecturer]
    
    def get_queryset(self):
        return Issue.objects.filter(assigned_to=self.request.user.lecturer_profile)
    
    def perform_update(self, serializer):
        issue = serializer.save()
        
        # Send notification about status change
        if issue.status == 'resolved':
            create_notification(
                recipient=issue.student.user,
                notification_type='issue_resolved',
                issue=issue,
                message=f'Your issue "{issue.title}" has been resolved by {self.request.user.get_full_name()}.'
            )
        else:
            create_notification(
                recipient=issue.student.user,
                notification_type='issue_updated',
                issue=issue,
                message=f'Your issue "{issue.title}" has been updated by {self.request.user.get_full_name()}.'
            )


class AcademicRegistrarIssueListView(generics.ListAPIView):
    """Get list of all issues for registrar"""
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAcademicRegistrar]


class AcademicRegistrarIssueDetailView(generics.RetrieveUpdateAPIView):
    """View and update any issue as registrar"""
    serializer_class = IssueSerializer
    permission_classes = [IsAcademicRegistrar]
    queryset = Issue.objects.all()
    
    def perform_update(self, serializer):
        issue = serializer.save()
        
        # Send notifications about changes
        if issue.status == 'resolved':
            # Notify student
            create_notification(
                recipient=issue.student.user,
                notification_type='issue_resolved',
                issue=issue,
                message=f'Your issue "{issue.title}" has been resolved by the registrar.'
            )
            
            # Notify lecturer if assigned
            if issue.assigned_to:
                create_notification(
                    recipient=issue.assigned_to.user,
                    notification_type='issue_resolved',
                    issue=issue,
                    message=f'Issue "{issue.title}" has been resolved by the registrar.'
                )
        else:
            # Notify about other updates
            create_notification(
                recipient=issue.student.user,
                notification_type='issue_updated',
                issue=issue,
                message=f'Your issue "{issue.title}" has been updated by the registrar.'
            )


class IssueDeleteView(generics.DestroyAPIView):
    """Delete an issue"""
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Only allow users to delete their own issues
        if self.request.user.role == 'student':
            return Issue.objects.filter(student=self.request.user.student_profile)
        elif self.request.user.role == 'registrar':
            return Issue.objects.all()
        return Issue.objects.none()
    
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response({
                'error': 'Failed to delete issue'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Notification related views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    """Get user's notifications"""
    try:
        notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({
            'error': 'Failed to fetch notifications'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    try:
        notification = Notification.objects.get(id=notification_id, recipient=request.user)
        notification.is_read = True
        notification.save()
        return Response({'status': 'success'})
    except Notification.DoesNotExist:
        return Response({
            'error': 'Notification not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': 'Failed to mark notification as read'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_unread_count(request):
    """Get count of unread notifications"""
    try:
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return Response({'count': count})
    except Exception as e:
        return Response({
            'error': 'Failed to get unread count'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_notification(request, notification_id):
    """Delete a notification"""
    try:
        notification = Notification.objects.get(id=notification_id, recipient=request.user)
        notification.delete()
        return Response({'status': 'success'})
    except Notification.DoesNotExist:
        return Response({
            'error': 'Notification not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': 'Failed to delete notification'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_all_notifications(request):
    """Delete all notifications for a user"""
    try:
        Notification.objects.filter(recipient=request.user).delete()
        return Response({'status': 'success'})
    except Exception as e:
        return Response({
            'error': 'Failed to clear notifications'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def create_notification(recipient, notification_type, issue, message):
    """Helper function to create a new notification"""
    try:
        notification = Notification.objects.create(
            recipient=recipient,
            notification_type=notification_type,
            issue=issue,
            message=message
        )
        return notification
    except Exception as e:
        print(f"Error creating notification: {str(e)}")
        return None


# Issue management views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_issue(request):
    """Create a new issue"""
    try:
        serializer = IssueSerializer(data=request.data)
        if serializer.is_valid():
            issue = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': 'Failed to create issue'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_issue(request, issue_id):
    """Update an existing issue"""
    try:
        issue = Issue.objects.get(pk=issue_id)
        serializer = IssueSerializer(issue, data=request.data, partial=True)
        
        if serializer.is_valid():
            updated_issue = serializer.save()
            
            # Send notifications about changes
            if 'status' in request.data:
                if request.data['status'] == 'resolved':
                    create_notification(
                        recipient=issue.student.user,
                        notification_type='issue_resolved',
                        issue=updated_issue,
                        message=f'Your issue "{updated_issue.title}" has been resolved.'
                    )
                else:
                    create_notification(
                        recipient=issue.student.user,
                        notification_type='issue_updated',
                        issue=updated_issue,
                        message=f'Your issue "{updated_issue.title}" has been updated.'
                    )
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Issue.DoesNotExist:
        return Response({
            'error': 'Issue not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': 'Failed to update issue'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Student and Lecturer management views
class StudentListView(generics.ListAPIView):
    """Get list of all students"""
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsAcademicRegistrar | IsLecturer]
    
    def get_queryset(self):
        return Student.objects.all()


class LecturerListView(generics.ListAPIView):
    """Get list of all lecturers"""
    serializer_class = LecturerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Lecturer.objects.all()


class LecturerUpdateView(generics.UpdateAPIView):
    """Update lecturer details"""
    serializer_class = LecturerSerializer
    permission_classes = [IsAuthenticated, IsAcademicRegistrar]
    queryset = Lecturer.objects.all()
    
    def perform_update(self, serializer):
        serializer.save()


class LecturerDeleteView(generics.DestroyAPIView):
    """Delete a lecturer"""
    serializer_class = LecturerSerializer
    permission_classes = [IsAuthenticated, IsAcademicRegistrar]
    queryset = Lecturer.objects.all()
    
    def perform_destroy(self, instance):
        instance.user.delete()  # This will cascade delete the lecturer profile


def home(request):
    """Home page view"""
    return render(request, 'home.html')


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_issue_status(request, pk):
    """Update the status of an issue"""
    try:
        issue = Issue.objects.get(pk=pk)
        new_status = request.data.get('status')
        
        if not new_status:
            return Response({
                'error': 'Status is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        issue.status = new_status
        issue.save()
        
        # Send notification about status change
        if new_status == 'resolved':
            create_notification(
                recipient=issue.student.user,
                notification_type='issue_resolved',
                issue=issue,
                message=f'Your issue "{issue.title}" has been marked as resolved.'
            )
        
        return Response({'status': 'success'})
    
    except Issue.DoesNotExist:
        return Response({
            'error': 'Issue not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': 'Failed to update issue status'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
