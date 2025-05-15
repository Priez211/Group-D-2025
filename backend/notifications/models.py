from django.db import models
from django.utils import timezone
from django.conf import settings

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('issue_created', 'New Issue Created'),
        ('issue_updated', 'Issue Updated'),
        ('issue_resolved', 'Issue Resolved'),
        ('issue_assigned', 'Issue Assigned'),
        ('comment_added', 'New Comment Added'),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    issue = models.ForeignKey('aits.Issue', on_delete=models.CASCADE, related_name='issue_notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.notification_type} for {self.recipient.username}" 