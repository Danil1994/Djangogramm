from pathlib import Path
from typing import Union

from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
from django.forms import modelformset_factory

from main_app.constants import allowed_photos_extensions
from main_app.models import Comment, CustomUser, Photo, Post, Tag


def validate_image_extension(value: Union[bytes, str, memoryview]) -> None:
    extension = Path(value.name).suffix.lower()

    if extension.lower() not in allowed_photos_extensions:
        raise forms.ValidationError('Invalid file extension.')


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image',)

    image = forms.ImageField(validators=[validate_image_extension])


PhotoFormSet = modelformset_factory(Photo, form=PhotoForm, extra=5)


# Form for creating and updating Post objects
class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('name', 'summary',)  # Fields to include in the form


# Form for creating and updating Tag objects
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('tag',)  # Fields to include in the form


# Form for authenticating users via email and password
class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(),
                                label='Email')  # Customizing the username field to accept emails

    class Meta:
        fields = ('email', 'password')  # Fields to include in the form


# Form for creating new CustomUser objects (user registration form)
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "bio", "avatar")  # Fields to include in the form


# Form for updating existing CustomUser objects (user profile editing form)
class CustomUserChangeForm(UserChangeForm):
    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    # Additional avatar field allowing users to upload their profile picture

    class Meta:
        model = CustomUser
        fields = ("username", "email", "bio", "avatar")  # Fields to include in the form


# Form for creating and updating Comment objects
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)  # Fields to include in the form
