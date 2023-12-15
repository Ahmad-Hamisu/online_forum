from django.apps import AppConfig
from django.apps import apps


class ForumappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'forumapp'

    def ready(self):
        # Check if the 'auth' app is installed
        if apps.is_installed('auth'):
            from django.contrib.auth.models import Group
            moderator_group, created = Group.objects.get_or_create(
                name='Moderator')
