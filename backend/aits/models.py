from django.db import models
from django.contrib.auth.models import AbstractUser
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
    department = models.CharField(max_length=50, choices= DEPARTMENT_CHOICES)
    staff_id = models.CharField(max_length=20, null=True, blank=True)
    student_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.user_type})"

