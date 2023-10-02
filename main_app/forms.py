import os

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import modelformset_factory

from main_app.models import Comment, CustomUser, Photo, Post, Tag


def validate_image_extension(value):
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']  # Расширения файлов, которые разрешены
    extension = os.path.splitext(value.name)[1]  # Получаем расширение загруженного файла

    if extension.lower() not in allowed_extensions:
        raise forms.ValidationError('Недопустимое расширение файла. Разрешены только .jpg, .jpeg, .png, .gif.')


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']

    image = forms.ImageField(validators=[validate_image_extension])


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
