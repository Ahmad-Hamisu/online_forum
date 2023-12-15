# views.py
from django.shortcuts import render, get_object_or_404
from .models import UserProfile  # Assuming you have a UserProfile model
from django.contrib import messages
from .models import UserProfile
from .forms import SignupForm

from .models import CustomUser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Group
from .models import Topic, Reply, Notification
from .models import Notification
from django.db.models import Q
from .forms import ReportForm
from .models import Post, Reply
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Reply
from .forms import ReplyForm
from .models import Category, Topic
from django.shortcuts import render
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm


def home(request):
    return render(request, 'home.html')


@login_required
def user_profile(request):
    user = CustomUser.objects.get(username=request.user.username)
    context = {'user': user}
    return render(request, 'user_profile.html', context)

# views.py


@login_required
def current_user_profile(request):
    user = CustomUser.objects.get(username=request.user.username)
    context = {'user': user}
    return render(request, 'user_profile.html', context)


@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user)

    context = {'user_profile': user_profile}
    return render(request, 'profile/profile.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to your home page
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')  # Redirect to your home page
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


@login_required
def view_notifications(request):
    notifications = Notification.objects.filter(
        user=request.user).order_by('-timestamp')

    notifications.update(read=True)

    context = {
        'notifications': notifications,
    }

    return render(request, 'view_notifications.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'profile/edit_profile.html', {'form': form})


def edit_profile(request):
    return redirect('/forumapp/profile/')


def topics_in_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    topics = Topic.objects.filter(category=category)
    return render(request, 'forum/topics_in_category.html', {'category': category, 'topics': topics})


def topic_detail(request, topic_id):
    topic = Topic.objects.get(pk=topic_id)
    return render(request, 'forum/topic_detail.html', {'topic': topic})


@login_required
def post_reply(request, topic_id):
    topic = Topic.objects.get(pk=topic_id)

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.created_by = request.user
            reply.topic = topic
            reply.save()
            return redirect('topic_detail', topic_id=topic.id)
    else:
        form = ReplyForm()

    return render(request, 'forum/post_reply.html', {'form': form, 'topic': topic})


@login_required
def upvote_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.upvotes += 1
    post.save()
    return redirect('topic_detail', topic_id=post.topic.id)


@login_required
def downvote_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.downvotes += 1
    post.save()
    return redirect('topic_detail', topic_id=post.topic.id)


@login_required
def upvote_reply(request, reply_id):
    reply = Reply.objects.get(pk=reply_id)
    reply.upvotes += 1
    reply.save()
    return redirect('topic_detail', topic_id=reply.topic.id)


@login_required
def downvote_reply(request, reply_id):
    reply = Reply.objects.get(pk=reply_id)
    reply.downvotes += 1
    reply.save()
    return redirect('topic_detail', topic_id=reply.topic.id)


@login_required
def hide_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.is_hidden = True
    post.save()
    return redirect('topic_detail', topic_id=post.topic.id)


@login_required
def unhide_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.is_hidden = False
    post.save()
    return redirect('topic_detail', topic_id=post.topic.id)


@login_required
def hide_reply(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    reply.is_hidden = True
    reply.save()
    return redirect('topic_detail', topic_id=reply.topic.id)


@login_required
def unhide_reply(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    reply.is_hidden = False
    reply.save()
    return redirect('topic_detail', topic_id=reply.topic.id)


@login_required
def report_content(request, post_id=None, reply_id=None):
    if post_id:
        content_object = get_object_or_404(Post, pk=post_id)
    elif reply_id:
        content_object = get_object_or_404(Reply, pk=reply_id)
    else:
        return redirect('home')

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.created_by = request.user
            report.save()

            return redirect('home')
    else:
        form = ReportForm(initial={'post': post_id, 'reply': reply_id})

    return render(request, 'forum/report_content.html', {'form': form, 'content_object': content_object})


def search_topics(request):
    query = request.GET.get('q')
    filter_category = request.GET.get('category')
    filter_tag = request.GET.get('tag')

    topics = Topic.objects.all()

    if query:
        topics = topics.filter(Q(title__icontains=query) | Q(
            posts__content__icontains=query) | Q(replies__content__icontains=query)).distinct()

    if filter_category:
        topics = topics.filter(category__name=filter_category)

    if filter_tag:
        topics = topics.filter(tags__name=filter_tag)

    return render(request, 'forum/search_topics.html', {'topics': topics, 'query': query})


@login_required
def view_notifications(request):
    notifications = Notification.objects.filter(
        user=request.user, is_read=False)
    return render(request, 'forum/notifications.html', {'notifications': notifications})


@login_required
def post_reply(request, topic_id):
    topic = Topic.objects.get(pk=topic_id)

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.created_by = request.user
            reply.topic = topic
            reply.save()

            if request.user != topic.created_by:
                content = f"New reply by {request.user.username} in your topic: '{topic.title}'"
                Notification.objects.create(
                    user=topic.created_by, content=content)

            return redirect('topic_detail', topic_id=topic.id)
    else:
        form = ReplyForm()

    return render(request, 'forum/post_reply.html', {'form': form, 'topic': topic})


def view_topics(request):
    topics_list = Topic.objects.all().order_by('-created_at')
    paginator = Paginator(topics_list, 10)

    page = request.GET.get('page')
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)

    return render(request, 'forum/view_topics.html', {'topics': topics})


def topic_detail(request, topic_id):
    topic = Topic.objects.get(pk=topic_id)
    replies_list = Reply.objects.filter(topic=topic).order_by('created_at')
    paginator = Paginator(replies_list, 10)
    page = request.GET.get('page')
    try:
        replies = paginator.page(page)
    except PageNotAnInteger:
        replies = paginator.page(1)
    except EmptyPage:
        replies = paginator.page(paginator.num_pages)

    return render(request, 'forum/topic_detail.html', {'topic': topic, 'replies': replies})


@user_passes_test(lambda u: u.is_moderator)
def moderator_only_view(request):
    pass


def my_view(request):
    if request.user.is_admin:
        pass
    elif request.user.is_moderator:
        pass
    else:
        pass


def assign_moderator_role(username):
    user = User.objects.get(username=username)
    moderator_group = Group.objects.get(name='Moderator')
    user.groups.add(moderator_group)
