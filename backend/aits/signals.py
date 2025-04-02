from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Issue,Notifications

@receiver(post_save,sender=Issue)
def issue_notification(sender,instance,created,**kwargs):
    if created:
        message=f"A new issue'{instance.title}'has been created"
        notification_type="New Issue Created"
    else:
        message=f"Your issue'{instance.title}'has been updated."
        notification_type="Issue Updated"
    Notifications.objects.create(
        receipient=instance.student,
        notification_type=notification_type,
        message=message

    )