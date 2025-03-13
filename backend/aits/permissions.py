from rest_framework import permissions
class IsRegistrar(permissions.BasePermission):
    def has_permissions(self,request,view):
        return request.user.is_authenticated and request.user.user_type=='registrar'
class Islecturer(permissions.BasePermission):
    def has_permissions(self,request,view):
        return request.user.is_authenticated and request.user.user_type=='lecturer'
class Isstudent(permissions.BasePermission):
    def has_permissions(self,request,view):
        return request.user.is_authenticated and request.user.user_type=='student'
class IsOwnerOrReadOnly(permissions.BasePermission):
    #it only allows the user who has submitted the issue to update or delete the issue
    def has_object_permissions(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.student==request.user



