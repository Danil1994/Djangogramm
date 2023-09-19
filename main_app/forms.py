from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import modelformset_factory

from .models import Comment, CustomUser, Photo, Post, Tag


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']


PhotoFormSet = modelformset_factory(Photo, form=PhotoForm, extra=5)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'summary', ]


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "bio", "avatar")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "bio", "avatar")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('tag',)
