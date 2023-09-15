from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser, Photo, Post


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'summary', 'tag', ]


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "bio", "avatar")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "bio", "avatar")
