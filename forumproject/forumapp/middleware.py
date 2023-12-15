# middleware.py
from django.contrib.auth.models import Group


class UserRoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.is_admin = request.user.groups.filter(name='Admin').exists()
        request.is_moderator = request.user.groups.filter(
            name='Moderator').exists()
        return self.get_response(request)
