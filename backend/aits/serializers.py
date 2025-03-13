from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Issue, Department
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
        fields=['issue_id','title','description','status','priority','created_at','updated_at','student','assigned_to','resolved_by','attachment','Lecturer_comment','resolved_at']
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
        fields=['deparment_id','name','faculty']
