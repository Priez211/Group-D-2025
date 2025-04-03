from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Issue, Department,Notifications,Student,AcademicRegistrar,Lecturer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

User=get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['id', 'username', 'email', 'role', 'first_name', 'last_name']


class StudentSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Student
        fields = ['id', 'user']


class AcademicRegistrarSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=AcademicRegistrar
        fields = ['id', 'user']


class LecturerSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Lecturer
        fields = ['id', 'user', 'department']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'faculty']


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
        fields=['id','title','category','description','status', 'priority','courseUnit','yearOfStudy','semester','student','assigned_to','created_at','updated_at','attachment']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Department
        fields=['id','name']

class NotificationsSerializer(serializers.ModelSerializer):
    recipient=UserSerializer()
    related_issue=IssueSerializer()
    class Meta:
        model=Notifications
        fields=['id', 'recipient', 'type', 'title', 'message', 'created_at', 'read', 'related_issue']

class SignupSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,required=True,min_length=8)
    class Meta:
        model=User
        fields=['username','password','user_type','student_number','email','full_name']
        def create(self, validated_data):
            validated_data['password']=make_password(validated_data['password'])
            return super().create(validated_data)

class StudentRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    student_data = serializers.DictField()

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "This email already exist"})
        if User.objects.filter(name=data['username']).exists():
            raise serializers.ValidationError({"username": "This Username already exist"})
        #validate student data

        student_data = data.get('student_data', {})
        required_fields = ['college', 'department', 'year_of_study', 'course']
        for field in required_fields:
            if field  not in student_data:
                raise serializers.ValidationError({f"student_data.{field}": f"{field} is required"})
        return data
    def create(self, validated_data):
        try:
            #removes student_data from validate data for seperating process
            
            student_data = validated_data.pop('student_data')
            
            #creating the user instance
            user = User.objects.create(
                username = validated_data['username'],
                email = validated_data['email'],
                first_name = validated_data['first_name'],
                last_name=validated_data['last_name'],
                password=make_password(validated_data['password']),
                role='student',
            )

            #create/ get department
            department_name = student_data['department']
            try:
                department = Department.objects.get(name = department_name)
            except Department.DoesNotExist:
                college = 'College of Computing' 
                department = Department.objects.create(
                    name = department_name,
                    college = college
                )
            #creating the student instance with all the dat
            student = Student.objects.create(
                user = user,
                college = student_data['college'],
                department = department,
                year_of_study = student_data['year_of_study'],
                course = student_data['course']
            )
            return student
            
        except Exception as e:
            #if and error occurs during student creation, delete
            if 'user' in locals():
                user.delete()
            raise serializers.ValidationError(str(e))

class RegistrarRegistrationSerializers(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    registrar_data = serializers.DictField()

    def validate(self, data):
        if User.objects.filter(email = data['email'].exists()):
            raise serializers.ValidationError({"email": "This email already exist"})
        
        if User.objects.filter(username = data['username'].exists()):
            raise serializers.ValidationError({"username": "Username already exist"})
        
        registrar_data = data.get('registrar_data', {})
        required_fields = ['college', 'department']
        for field in required_fields:
            if field not in required_fields:
                raise serializers.ValidationError({f"registrar_data.{field}": f"{field} is required"})
        return data
    
    def create(self, validated_data):
        try:
            # Extract registrar data
            registrar_data = validated_data.pop('registrar_data')
            
            # Create User instance
            user = User.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                role='registrar',
                password=make_password(validated_data['password'])
            )
            
            # Get or create Department instance
            department_name = registrar_data['department']
            try:
                department = Department.objects.get(name=department_name)
            except Department.DoesNotExist:
                # If department doesn't exist, create it with appropriate faculty
                college = "College of Computing"  
                department = Department.objects.create(
                    name=department_name,
                    college = college
                )
            
            # Creating AcademicRegistrar instance with additional data
            registrar = AcademicRegistrar.objects.create(
                user=user,
                college=registrar_data['college'],
                department=department
            )
            return registrar
        except Exception as e:
            # If any error occurs during user creation, delete the user if it was created
            if 'user' in locals():
                user.delete()
            raise serializers.ValidationError(str(e))
        

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)

    def validate(self,data):

        User=authenticate(username=data['username'],password=data['password'])
        if User is None:
            raise serializers.ValidationError('Invalid credentials')
        refresh=RefreshToken.for_user(User)
        role="Unknown"
        if hasattr(User,'student'):
            role="Student"
        elif hasattr(User,'academicregistrar'):
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

class LogoutSerializer(serializers.ModelSerializer):
    #validaates the refresh token
    def validate(self,data):
        try:
            RefreshToken(data["refresh"]).blacklist()
        except Exception as e:
            raise serializers.ValidationError('Invalid or expired token')
        return data
        
