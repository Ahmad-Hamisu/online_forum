# forms.py
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Report
from .models import Post, Reply
from ckeditor.widgets import CKEditorWidget
from .models import Reply
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = ['content']


class UpvoteForm(forms.Form):
    pass


class DownvoteForm(forms.Form):
    pass


class SearchForm(forms.Form):
    query = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Search topics...'}))
    filter_category = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Filter by category...'}))
    filter_tag = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Filter by tag...'}))


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['content', 'post', 'reply']


class ReplyForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Reply
        fields = ['content']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        # Add any additional fields you want to include in the form
        fields = ['bio', 'avatar']


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 rounded-xl'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 rounded-xl'
    }))


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 rounded-xl'
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address',
        'class': 'w-full py-4 rounded-xl'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 rounded-xl'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password',
        'class': 'w-full py-4 rounded-xl'
    }))
