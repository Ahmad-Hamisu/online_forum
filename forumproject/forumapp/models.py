# models.py
from django.apps import apps
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission
from .utils import get_related_model
from django.conf import settings

from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    # Add related_name to avoid clashes
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_user_set')


# models.py


class Category(models.Model):
    name = models.CharField(max_length=255)
    related_model = models.ForeignKey(
        'forumapp.RelatedModel', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_related_model(self):
        # Import the model inside the function
        from .models import RelatedModel
        return RelatedModel

    def do_something_with_related_model(self):
        related_model = self.get_related_model()
        # ... do something with related_model


class RelatedModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Add other fields as needed
    some_field = models.CharField(max_length=100)
    another_field = models.IntegerField()
    boolean_field = models.BooleanField(default=False)
    # Add more fields based on your requirements

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Topic(models.Model):
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


class Post(models.Model):
    content = models.TextField()
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    is_hidden = models.BooleanField(default=False)  # New field
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(
        Topic, related_name='posts', on_delete=models.CASCADE)

    def calculate_score(self):
        return self.upvotes - self.downvotes

    def __str__(self):
        return f"{self.created_by.username}'s post on {self.topic.title}"


class Reply(models.Model):
    content = models.TextField()
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    is_hidden = models.BooleanField(default=False)  # New field
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(
        Topic, related_name='replies', on_delete=models.CASCADE)

    def calculate_score(self):
        return self.upvotes - self.downvotes

    def __str__(self):
        return f"{self.created_by.username}'s reply on {self.topic.title}"


class Report(models.Model):
    content = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        Post, null=True, blank=True, on_delete=models.CASCADE)
    reply = models.ForeignKey(
        Reply, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Report by {self.created_by.username}"


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"
