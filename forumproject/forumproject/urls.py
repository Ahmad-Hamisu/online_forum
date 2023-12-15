"""forumproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from forumapp.views import user_profile, current_user_profile, home, profile, register, topic_detail, post_reply, view_topics, report_content, search_topics
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('forumapp/', include('forumapp.urls', namespace='forumapp')),
    path('profile/', profile, name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    path('accounts/profile/', current_user_profile, name='current_user_profile'),
    path('profile/<str:username>/', user_profile, name='user_profile'),
    path('topic/<int:topic_id>/', topic_detail, name='topic_detail'),
    path('topic/<int:topic_id>/post-reply/', post_reply, name='post_reply'),
    path('report-content/', report_content, name='report_content'),
    path('search-topics/', search_topics, name='search_topics'),
    path('view-topics/', view_topics, name='view_topics'),


]
