from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone


class Department(models.Model):
    DEPARTMENT_NAMES = (
        ('computer_science', 'Computer Science'),
        ('software_engineering', 'Software Engineering'),
        ('information_technology', 'Information Technology'),
        ('library_and_information', 'Library And Information'),
    )

    department_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, choices= DEPARTMENT_NAMES, default='computer_science')

    def __str__(self):
        return f"{self.name} - {self.faculty}"

    class Meta:
        ordering = ['name']



class User(AbstractUser):
    USER_TYPES = (
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('registrar', 'Registrar'),
    )

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
    
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    email = models.EmailField(max_length=55)
    full_name = models.CharField(max_length=255)
    staff_id = models.CharField(max_length=20, null=True, blank=True)
    student_number = models.CharField(max_length=20, null=True, blank=True)

    college = models.CharField(max_length=255, choices=COLLEGE_CHOICES, blank=True, null=True)
    department = models.ForeignKey(Department, max_length=50, on_delete=models.CASCADE)
    year_of_study = models.CharField(max_length=50, choices=YEAR_CHOICES, blank=True, null=True)
    course = models.CharField(max_length=255, choices=COURSE_CHOICES, blank=True, null=True)

    USERNAME_FIELD = 'full_name'
    REQUIRED_FIELDS = ['username', 'full_name', 'student_number', 'staff_id', 'role']

    # Unique related_name attributes to avoid clashes
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="aits_user_groups",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="aits_user_permissions",
        related_query_name="user",
    )

    def __str__(self):
        return f"{self.get_full_name()} ({self.user_type})"

class Student(User):
    YEAR_CHOICES = (
        ('First Year', 'First Year'),
        ('Second Year', 'Second Year'),
        ('Third Year', 'Third Year'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='students')
    year_of_study = models.CharField(max_length=20, choices=YEAR_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()

class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lecturer_profile')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='lecturers')

    def __str__(self):
        return self.user.get_full_name()
    
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

class Issue(models.Model):
    CATEGORY_CHOICES = [
        ('missing_mark', 'Missing Mark'),
        ('ask_fro_re_do', 'Ask for Re-do'),
        ('wrong_marks', 'Wrong Marks'),
        ('other', 'Other'),
    ] 

    STATUS_CHOICES = (
        ('opened', 'Opened'),
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('declined', 'Declined'),
    )

    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    COURSE_UNITS = (
        ('CSC1100', 'CSC1100 - System Analysis And Design'),
        ('CSC1200', 'CSC1200 - Data Structures'),
        ('CSC2100', 'CSC2100 - Operating Systems'),
        ('CSC2200', 'CSC2200 - Software Development Project'),
        ('CSC3100', 'CSC3100 - Probability And Statistics'),
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

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='missing_mark')
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_issues', limit_choices_to={'user_type': 'student'})
    courseUnit = models.CharField(max_length=10, choices=COURSE_UNITS, null=True, blank=True)
    yearOfStudy = models.CharField(max_length=1, choices=YEARS_OF_STUDY, null=True, blank=True)
    semester = models.CharField(max_length=1, choices=SEMESTERS, null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    attachment = models.FileField(upload_to='issue_attachments/', null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_issues', limit_choices_to={'user_type': 'lecturer'})
    lecturer_comment = models.TextField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_issues')

    def __str__(self):
        return self.title
    
    def resolve(self, user, comment=None):
        self.status = 'resolved'
        self.resolved_by = user
        self.resolved_at = timezone.now()
        if comment:
            self.lecturer_comment = comment
        self.save()
    
    def get_priority_for_category(self):
        return self.CATEGORY_PRIORITY_MAP.get(self.category, 'low')

    def save(self, *args, **kwargs):
        if not self.priority or self.priority == '':
            self.priority = self.get_priority_for_category()
        super().save(*args, **kwargs)

class Notifications(models.Model):
    NOTIFICATION_TYPES = (
        ('issue_update', 'Issue Update'),
        ('issue_assigned', 'Issue Assigned'),
        ('announcement', 'Announcement'),
        ('other', 'Other')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=15, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    related_issue = models.ForeignKey(Issue, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
