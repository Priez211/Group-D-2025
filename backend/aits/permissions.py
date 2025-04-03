from rest_framework import permissions
from .models import Issue, Lecturer, Student, Lecturer, AcademicRegistrar, Department

class IsRegistrar(permissions.BasePermission):
    def has_permission(self,request,view):
        return bool(request.user.is_authenticated and request.user.user_role=='registrar')

    def has_object_permission(self, obj, request, view):
        if isinstance(obj, Issue):
            registrar = AcademicRegistrar.objects.get(user = request.user)
            return obj.student.user.college == registrar.college
        return False

class Islecturer(permissions.BasePermission):
    def has_permission(self,request,view):
        return bool(request.user.is_authenticated and request.user.user_role=='lecturer')
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Issue):
            lecturer = Lecturer.objects.get(user = request.user)
            return obj.student.user.department == lecturer.department
        return False

class Isstudent(permissions.BasePermission):
    def has_permission(self,request,view):
        return bool(request.user.is_authenticated and request.user.user_role=='student')

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Issue):
            obj.student.user == request.user
        return False