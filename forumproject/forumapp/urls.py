# urls.py
from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from . import views

from .views import (
    edit_profile, user_profile, topics_in_category, topic_detail,
    post_reply, upvote_post, downvote_post, upvote_reply, downvote_reply,
    hide_post, unhide_post, hide_reply, unhide_reply, report_content,
    search_topics, view_notifications, profile
)
from django.conf import settings
from django.conf.urls.static import static

app_name = 'forumapp'

urlpatterns = [
         path('', views.home, name='home'),  
    path('user-profile/', user_profile, name='user_profile'),
    path('view-notifications/', view_notifications, name='view_notifications'),

    path('notifications/', view_notifications, name='view_notifications'),
    path('search/', search_topics, name='search_topics'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('profile/', profile, name='profile'),
    path('reset/done/', PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('profile/<str:username>/', user_profile, name='user_profile'),
    path('category/<int:category_id>/',
         topics_in_category, name='topics_in_category'),

    path('topic/<int:topic_id>/', topic_detail, name='topic_detail'),
    path('topic/<int:topic_id>/post_reply/', post_reply, name='post_reply'),
    path('post/<int:post_id>/upvote/', upvote_post, name='upvote_post'),
    path('post/<int:post_id>/downvote/', downvote_post, name='downvote_post'),
    path('reply/<int:reply_id>/upvote/', upvote_reply, name='upvote_reply'),
    path('reply/<int:reply_id>/downvote/',
         downvote_reply, name='downvote_reply'),
    path('post/<int:post_id>/hide/', hide_post, name='hide_post'),
    path('post/<int:post_id>/unhide/', unhide_post, name='unhide_post'),
    path('reply/<int:reply_id>/hide/', hide_reply, name='hide_reply'),
    path('reply/<int:reply_id>/unhide/', unhide_reply, name='unhide_reply'),
    path('report_content/', report_content, name='report_content'),
    path('post/<int:post_id>/report/', report_content, name='report_post'),
    path('reply/<int:reply_id>/report/', report_content, name='report_reply'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
