from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import check_password
from django.conf import settings
import jwt
import datetime
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from  rest_framework import serializers

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
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            role = serializer.validated_data['role']
            
            # Get current timestamp and set expiration
            now = datetime.datetime.utcnow()
            exp = now + datetime.timedelta(hours=24)
            
            # Generate JWT token with expiration
            token = jwt.encode(
                {
                    'user_id': user.username,
                    'role': role,
                    'exp': int(exp.timestamp())
                },
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
            }, status=status.HTTP_200_OK)
            
        return Response(
            {'error': serializer.errors.get('non_field_errors', ['Invalid credentials'])[0]},
            status=status.HTTP_401_UNAUTHORIZED
        )


        
        


class RegisterView(APIView):
    permission_classes = [AllowAny]
    role_serializers = {
        'student': StudentRegistrationSerializer,
        'lecturer': LecturerRegistrationSerializer,
        'registrar': RegistrarRegistrationSerializer
    }
    
    def post(self, request):
        role = request.data.get('role')
        serializer_class = self.role_serializers.get(role)
        
        if not serializer_class:
            return Response(
                {'error': 'Invalid role. Must be one of: student, lecturer, registrar'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        
        return Response({
            'message': 'Registration successful',
            'user': {
                'userId': instance.user.username,
                'fullName': f"{instance.user.first_name} {instance.user.last_name}".strip(),
                'email': instance.user.email,
                'role': instance.user.role
            }
        }, status=status.HTTP_201_CREATED)


class StudentIssueCreateView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    def get(self, request):
        student = request.user.student_profile
        issues = Issue.objects.filter(student=student).order_by('-created_at')
        return Response({'issues': IssueSerializer(issues, many=True).data})
    
    def post(self, request):
        student = request.user.student_profile
        assigned_to = None
        
        if 'assigned_to' in request.data:
            try:
                assigned_to = Lecturer.objects.get(id=request.data['assigned_to'])
            except Lecturer.DoesNotExist:
                return Response(
                    {'error': 'Selected lecturer does not exist'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer = IssueSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        serializer.validated_data['student'] = student
        if assigned_to:
            serializer.validated_data['assigned_to'] = assigned_to
        
        if 'attachment' in request.FILES:
            serializer.validated_data['attachment'] = request.FILES['attachment']
        
        issue = serializer.save()
        
        # Create notifications
        create_notification(
            recipient=request.user,
            notification_type='issue_created',
            issue=issue,
            message=f'Your issue "{issue.title}" has been submitted successfully.'
        )
        
        if assigned_to:
            create_notification(
                recipient=assigned_to.user,
                notification_type='issue_assigned',
                issue=issue,
                message=f'You have been assigned a new issue: {issue.title}'
            )
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LecturerIssueListView(generics.ListAPIView):
    serializer_class = IssueSerializer
    permission_classes = [IsLecturer]

    def get_queryset(self):
        lecturer = self.request.user.lecturer_profile
        return Issue.objects.filter(assigned_to=lecturer)


class IssueUpdateView(generics.UpdateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsLecturer | IsAcademicRegistrar]

    def perform_update(self, serializer):
        issue = serializer.save()
        if self.request.user.role == 'lecturer':
            create_notification(
                recipient=issue.student.user,
                notification_type='issue_updated',
                issue=issue,
                message=f'Your issue "{issue.title}" has been updated'
            )


class StudentIssueDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = IssueSerializer
    permission_classes = [IsStudent]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        student = self.request.user.student_profile
        return Issue.objects.filter(student=student)

    def perform_update(self, serializer):
        student = self.request.user.student_profile
        
        if 'attachment' in self.request.FILES:
            serializer.validated_data['attachment'] = self.request.FILES['attachment']
            
        issue = serializer.save(student=student)
        
        if issue.assigned_to:
            create_notification(
                recipient=issue.assigned_to.user,
                notification_type='issue_updated',
                issue=issue,
                message=f'Issue updated: {issue.title}'
            )


class LecturerIssueDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = IssueSerializer
    permission_classes = [IsLecturer]

    def get_queryset(self):
        lecturer = self.request.user.lecturer_profile
        return Issue.objects.filter(assigned_to=lecturer)

    def perform_update(self, serializer):
        issue = serializer.save()
        
        if 'status' in self.request.data:
            create_notification(
                recipient=issue.student.user,
                notification_type='issue_updated',
                issue=issue,
                message=f'Your issue "{issue.title}" status has been updated to {issue.status}'
            )


class AcademicRegistrarIssueListView(generics.ListAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAcademicRegistrar]


class AcademicRegistrarIssueDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = IssueSerializer
    permission_classes = [IsAcademicRegistrar]
    queryset = Issue.objects.all()

    def perform_update(self, serializer):
        issue = serializer.save()
        
        if 'status' in self.request.data:
            create_notification(
                recipient=issue.student.user,
                notification_type='issue_updated',
                issue=issue,
                message=f'Your issue "{issue.title}" status has been updated to {issue.status}'
            )
        
        if 'assigned_to' in self.request.data and issue.assigned_to:
            create_notification(
                recipient=issue.assigned_to.user,
                notification_type='issue_assigned',
                issue=issue,
                message=f'You have been assigned to issue: {issue.title}'
            )


class IssueDeleteView(generics.DestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'registrar':
            return Issue.objects.all()
        elif self.request.user.role == 'student':
            return Issue.objects.filter(student__user=self.request.user)
        return Issue.objects.none()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Issue deleted successfully'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    return Response(NotificationSerializer(notifications, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return Response({'status': 'success'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_unread_count(request):
    count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return Response({'count': count})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_notification(request, notification_id):
    notification = Notification.objects.get(id=notification_id, recipient=request.user)
    notification.delete()
    return Response({'status': 'success'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_all_notifications(request):
    Notification.objects.filter(recipient=request.user).delete()
    return Response({'status': 'success'})


def create_notification(recipient, notification_type, issue, message):
    return Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        issue=issue,
        message=message
    )


class StudentListView(generics.ListAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsAcademicRegistrar | IsLecturer]
    
    def get_queryset(self):
        queryset = Student.objects.all().select_related('user', 'department')
        
        if self.request.user.role == 'lecturer':
            lecturer = self.request.user.lecturer_profile
            queryset = queryset.filter(college=lecturer.department.faculty)
            
        college = self.request.query_params.get('college')
        if college and college != 'All Colleges':
            queryset = queryset.filter(college=college)
            
        department = self.request.query_params.get('department')
        if department and department != 'All Departments':
            queryset = queryset.filter(department__name=department)
            
        year = self.request.query_params.get('year')
        if year and year != 'All Years':
            queryset = queryset.filter(year_of_study=year)
            
        return queryset


class LecturerListView(generics.ListAPIView):
    serializer_class = LecturerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Lecturer.objects.all().select_related('user', 'department')
        department = self.request.query_params.get('department')
        if department:
            queryset = queryset.filter(department__name=department)
        return queryset


class LecturerUpdateView(generics.UpdateAPIView):
    serializer_class = LecturerSerializer
    permission_classes = [IsAuthenticated, IsAcademicRegistrar]
    queryset = Lecturer.objects.all()

    def perform_update(self, serializer):
        lecturer = serializer.save()
        create_notification(
            recipient=lecturer.user,
            notification_type='profile_updated',
            issue=None,
            message=f'Your profile has been updated by {self.request.user.get_full_name()}'
        )


class LecturerDeleteView(generics.DestroyAPIView):
    serializer_class = LecturerSerializer
    permission_classes = [IsAuthenticated, IsAcademicRegistrar]
    queryset = Lecturer.objects.all()

    def perform_destroy(self, instance):
        user = instance.user
        instance.delete()
        user.delete()