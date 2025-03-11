from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone


class Department(models.Model):
    FACULTIES = (
        ('computer_science', 'Computer Science'),
        ('software_engineering', 'Software Engineering'),
        ('information_technology', 'Information Technology'),
        ('library_and_information', 'Library And Information'),
    )

    department_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    faculty = models.CharField(max_length=50, choices=FACULTIES)

    def __str__(self):
        return f"{self.name} - {self.faculty}"

    class Meta:
        ordering = ['name']

DEPARTMENT_CHOICES = [
    ('computer_science', 'Computer Science'),
    ('software_engineering', 'Software Engineering'),
    ('information_technology', 'Information Technology'),
    ('library_and_information', 'Library And Information'),
]

class User(AbstractUser):
    USER_TYPES = (
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('registrar', 'Registrar'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    staff_id = models.CharField(max_length=20, null=True, blank=True)
    student_number = models.CharField(max_length=20, null=True, blank=True)

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

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='missing_mark')
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_issues', limit_choices_to={'user_type': 'student'})
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_issues', limit_choices_to={'user_type': 'lecturer'})
    
    attachment = models.FileField(upload_to='issue_attachments/', null=True, blank=True)
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

class Notifications(models.Model):
    NOTIFICATION_TYPES = (
        ('issue_update', 'Issue Update'),
        ('issue_assigned', 'Issue Assigned'),
        ('announcement', 'Announcement'),
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
