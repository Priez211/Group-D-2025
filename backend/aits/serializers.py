from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Issue, Department,Notifications
from rest_framework_simplejwt.tokens import RefreshToken
User=get_user_model()
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
        fields=['id','title','description','status','priority','created_at','updated_at','student','assigned_to','resolved_by','lecturer_comment','attachment','resolved_at']
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
        fields=['id','name','faculty']
class NotificationsSerializer(serializers.ModelSerializer):
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
        return{
            'user':UserSerializer(User).data,
            'access_token':str(refresh.access_token),
            'refresh_token':str(refresh),
                      }
        
