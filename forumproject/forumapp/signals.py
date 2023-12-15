from django.db.models.signals import post_save
from .models import Notification
from .models import Reply
from django.dispatch import receiver

from django.db.models.signals import post_save
from .models import Notification
from django.dispatch import receiver


# Replace 'yourapp' with the actual name of your app
@receiver(post_save, sender='forumapp.Reply')
def create_notification(sender, instance, **kwargs):
    from .models import Reply  # Move the import inside the function

    if instance.created_by != instance.topic.created_by:
        content = f"New reply by {instance.created_by.username} in your topic: '{instance.topic.title}'"
        Notification.objects.create(
            user=instance.topic.created_by, content=content)
