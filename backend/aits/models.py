from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone

class User(AbstractUser):
    USER_TYPES = (
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('registrar', 'Registrar'),
    )

    DEPARTMENT_CHOICES = (
        ('computer_science', 'Computer Science'),
        ('software_engineering', 'Software Engineering'),
        ('information_technology', 'Information Technology'),
        ('information_system', 'Information System'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    staff_id = models.CharField(max_length=20, null=True, blank=True)
    student_number = models.CharField(max_length=20, null=True, blank=True)

    # Add unique related_name attributes to avoid clashes
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="aits_user_groups",  # Unique related_name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="aits_user_permissions",  # Unique related_name
        related_query_name="user",
    )

    def __str__(self):
        return f"{self.get_full_name()} ({self.user_type})"


class Issue(models.Model):
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
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_issues')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_issues')
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_issues')
    
    attachment = models.FileField(upload_to='issue_attachments/', null=True, blank=True)
    lecturer_comment = models.TextField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title