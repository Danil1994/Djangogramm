from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import modelformset_factory

from .models import CustomUser, Photo, Post


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']


PhotoFormSet = modelformset_factory(Photo, form=PhotoForm, extra=5)


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
