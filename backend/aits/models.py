from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model to handle different roles (Student, Lecturer, Academic Registrar)
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = (
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('registrar', 'Academic Registrar'),
    )
    role = models.CharField(max_length=10, choices=ROLES)
    email = models.EmailField(unique=True)

    # Add unique related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='aits_user_set',  # Unique related_name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='aits_user_set',  # Unique related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username


# Department model
class Department(models.Model):
    DEPARTMENT_CHOICES = (
        ('Department of Computer Science', 'Department of Computer Science'),
        ('Department Of Software Engineering', 'Department Of Software Engineering'),
        ('Department of Library And Information System', 'Department of Library And Information System'),
        ('Department Of Information Technology', 'Department Of Information Technology'),
    )
    name = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    faculty = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Lecturer model
class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lecturer_profile')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='lecturers')

    def __str__(self):
        return self.user.get_full_name()


# Student model
class Student(models.Model):
    COLLEGE_CHOICES = (
        ('College of Computing', 'College of Computing'),
        ('College Of Humanity And Social Sciences', 'College Of Humanity And Social Sciences'),
        ('College Of Engineering', 'College Of Engineering'),
        ('College Of Education', 'College Of Education'),
    )
    
    COURSE_CHOICES = (
        ('Computer Science', 'Computer Science'),
        ('Software Engineering', 'Software Engineering'),
        ('Library and Information', 'Library and Information'),
        ('Information Technology', 'Information Technology'),
    )
    
    YEAR_CHOICES = (
        ('First Year', 'First Year'),
        ('Second Year', 'Second Year'),
        ('Third Year', 'Third Year'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    college = models.CharField(max_length=100, choices=COLLEGE_CHOICES, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='students')
    year_of_study = models.CharField(max_length=20, choices=YEAR_CHOICES, blank=True, null=True)
    course = models.CharField(max_length=100, choices=COURSE_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()


# Academic Registrar model
class AcademicRegistrar(models.Model):
    COLLEGE_CHOICES = (
        ('College of Computing', 'College of Computing'),
        ('College Of Humanity And Social Sciences', 'College Of Humanity And Social Sciences'),
        ('College Of Engineering', 'College Of Engineering'),
        ('College Of Education', 'College Of Education'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='registrar_profile')
    college = models.CharField(max_length=100, choices=COLLEGE_CHOICES, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='registrars')

    def __str__(self):
        return self.user.get_full_name()


# Issue model
class Issue(models.Model):
    CATEGORIES = (
        ('academic', 'Academic Issues'),
        ('technical', 'Technical Issues'),
        ('administrative', 'Administrative Issues'),
        ('examination', 'Examination Issues'),
        ('registration', 'Registration Issues'),
        ('other', 'Other Issues'),
    )
    STATUSES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    )
    PRIORITIES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    COURSE_UNITS = (
        ('CSC1100', 'CSC1100 - Programming Fundamentals'),
        ('CSC1200', 'CSC1200 - Data Structures'),
        ('CSC2100', 'CSC2100 - Database Systems'),
        ('CSC2200', 'CSC2200 - Web Development'),
        ('CSC3100', 'CSC3100 - Software Engineering'),
    )
    YEARS_OF_STUDY = (
        ('1', 'First Year'),
        ('2', 'Second Year'),
        ('3', 'Third Year'),
        ('4', 'Fourth Year'),
    )
    SEMESTERS = (
        ('1', 'Semester 1'),
        ('2', 'Semester 2'),
    )

    CATEGORY_PRIORITY_MAP = {
        'academic': 'high',
        'examination': 'high',
        'technical': 'medium',
        'administrative': 'medium',
        'registration': 'medium',
        'other': 'low',
    }

    issue_id= models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUSES, default='open')
    priority = models.CharField(max_length=10, choices=PRIORITIES, null=True, blank=True)
    courseUnit = models.CharField(max_length=10, choices=COURSE_UNITS, null=True, blank=True)
    yearOfStudy = models.CharField(max_length=1, choices=YEARS_OF_STUDY, null=True, blank=True)
    semester = models.CharField(max_length=1, choices=SEMESTERS, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='issues')
    assigned_to = models.ForeignKey(Lecturer, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_issues')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_priority_for_category(self):
        return self.CATEGORY_PRIORITY_MAP.get(self.category, 'low')

    def save(self, *args, **kwargs):
        if not self.priority or self.priority == '':
            self.priority = self.get_priority_for_category()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Issue {self.issue_id} - {self.category}"

# Notification model
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('issue_created', 'New Issue Created'),
        ('issue_updated', 'Issue Updated'),
        ('issue_resolved', 'Issue Resolved'),
        ('issue_assigned', 'Issue Assigned'),
        ('comment_added', 'New Comment Added'),
    )

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.recipient.username} - {self.notification_type}"