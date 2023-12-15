# admin.py
from .models import RelatedModel
from django.contrib import admin
from .models import CustomUser, Category, Tag, Topic, Post, Reply, Report, Notification


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'bio', 'avatar')
    search_fields = ('username', 'email')
# forumapp/admin.py


admin.site.register(RelatedModel)


admin.site.register(CustomUser, CustomUserAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Category, CategoryAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Tag, TagAdmin)


class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'category')
    search_fields = ('title', 'created_by__username')


admin.site.register(Topic, TopicAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('content', 'upvotes', 'downvotes',
                    'is_hidden', 'created_by', 'created_at', 'topic')
    search_fields = ('content', 'created_by__username', 'topic__title')


admin.site.register(Post, PostAdmin)


class ReplyAdmin(admin.ModelAdmin):
    list_display = ('content', 'upvotes', 'downvotes',
                    'is_hidden', 'created_by', 'created_at', 'topic')
    search_fields = ('content', 'created_by__username', 'topic__title')


admin.site.register(Reply, ReplyAdmin)


class ReportAdmin(admin.ModelAdmin):
    list_display = ('content', 'created_by', 'created_at', 'post', 'reply')
    search_fields = ('content', 'created_by__username')


admin.site.register(Report, ReportAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'is_read', 'created_at')
    search_fields = ('user__username', 'content')


admin.site.register(Notification, NotificationAdmin)
