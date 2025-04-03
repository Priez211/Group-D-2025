from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Issue, Department,Notifications,Student,AcademicRegistrar,Lecturer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
User=get_user_model()
class SignupSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,required=True,min_length=8)
    class Meta:
        model=User
        fields=['username','password','user_type','student_number','email','full_name']
        def create(self,validated_data):
            validated_data['password']=make_password(validated_data['password'])
            return super().create(validated_data)
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','user_type','department','staff_id','student_number']
class IssueSerializer(serializers.ModelSerializer):
    student=UserSerializer(read_only=True)
    assigned_to=UserSerializer(read_only=True)
    resolved_by=UserSerializer(read_only=True)
    class  Meta:
        model=Issue
        fields=['id','title','category','description','status','priority','created_at','updated_at','student','assigned_to','resolved_by','lecturer_comment','attachment','resolved_at','semester','yearOfStudy','courseUnit']
class IssueCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Issue
        fields=['title','description','priority','attachment']
    def create(self,validated_data):
        request=self.context.get('request')
        validated_data['student']=request.user#assign logged-in user as a student
        return super().create(validated_data)

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Department
        fields=['id','name']
class NotificationsSerializer(serializers.ModelSerializer):
    recipient=UserSerializer()
    related_issue=IssueSerializer()
    class Meta:
        model=Notifications
        fields=['id', 'user', 'type', 'title', 'message', 'created_at', 'read', 'related_issue']
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)

    def validate(self,data):
        from django.contrib.auth import authenticate
        User=authenticate(username=data['username'],password=data['password'])
        if User is None:
            raise serializers.ValidationError('Invalid credentials')
        refresh=RefreshToken.for_user(User)
        role="Unknown"
        if hasattr(User,'student'):
            role="Student"
        elif hasattr(User,'registrar'):
            role="Acaddemic Registrar"
        elif hasattr(User,'lecturer'):
            role="Lecturer"

        return{
            'access':str(refresh.access_token),
            'refresh_token':str(refresh),
            'role':role,
            'user_id':User.id,
            'username':User.username,

                      }
class StudentSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Student
        fields='__all__'
class AcademicRegistrarSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=AcademicRegistrar
        fields='__all__'
class LecturerSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Lecturer
        fields='__all__'
class LogoutSerializer(serializers.ModelSerializer):
    #validaates the refresh token
    def validate(self,data):
        try:
            RefreshToken(data["refresh"]).blacklist()
        except Exception as e:
            raise serializers.ValidationError('Invalid or expired token')
        return data
        
