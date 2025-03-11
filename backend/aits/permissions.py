from rest_framework import permissions
class IsRegistrar(permissions.BasePermission):
    def has_permissions(self,request,view):
        return request.user.is_authenticated and request.user.user_type=='registrar'
