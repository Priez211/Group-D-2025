from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Issue
User=get_user_model()
class UserSerializer(serializers.ModelsSerializer):
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