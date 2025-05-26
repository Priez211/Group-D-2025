# Import required modules
from rest_framework import permissions
from .models import Issue, Lecturer, Student, AcademicRegistrar, Department


# Student permission class
class IsStudent(permissions.BasePermission):
    """Check if user is a student and has permission to access/modify resources"""
    
    def has_permission(self, request, view):
        # Check if user is authenticated and is a student
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'student'
        )

    def has_object_permission(self, request, view, obj):
        # Only allow access to student's own issues
        if isinstance(obj, Issue):
            return obj.student.user == request.user
        return False


# Lecturer permission class
class IsLecturer(permissions.BasePermission):
    """Check if user is a lecturer and has permission to access/modify resources"""
    
    def has_permission(self, request, view):
        # Check if user is authenticated and is a lecturer
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'lecturer'
        )

    def has_object_permission(self, request, view, obj):
        # Only allow access to issues assigned to this lecturer
        if isinstance(obj, Issue):
            lecturer = Lecturer.objects.get(user=request.user)
            return obj.assigned_to == lecturer
        return False


# Academic Registrar permission class
class IsAcademicRegistrar(permissions.BasePermission):
    """Check if user is an academic registrar and has permission to access/modify resources"""
    
    def has_permission(self, request, view):
        # Check if user is authenticated and is a registrar
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'registrar'
        )

    def has_object_permission(self, request, view, obj):
        # Registrars have access to all objects
        return True