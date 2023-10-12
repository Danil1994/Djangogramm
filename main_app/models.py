import pathlib
import uuid

import django
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def photo_file_path(instance: "Photo", filename: str):
    author_slug = slugify(instance.post.author.username)
    post_name_slug = slugify(instance.post.name)
    unique_filename = f"{author_slug}--{post_name_slug}--{uuid.uuid4()}" + pathlib.Path(filename).suffix
    return pathlib.Path('photos/') / unique_filename


class Photo(models.Model):
    image = models.ImageField(upload_to=photo_file_path, blank=True, null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.pk)


class Tag(models.Model):
    tag = models.CharField(max_length=50, primary_key=True, help_text="Enter tags separated by commas")

    def __str__(self):
        return self.tag


def avatar_file_path(instance: "CustomUser", filename: str):
    username_slug = slugify(instance.username)
    unique_filename = f"{username_slug}--{uuid.uuid4()}" + pathlib.Path(filename).suffix
    return pathlib.Path('avatars/') / unique_filename


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=1000, help_text='Introduce yourself', default=None, blank=True, null=True)
    avatar = models.ImageField(upload_to=avatar_file_path, default='avatars/base_avatar.png')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        """
        Returns the post`s url.
        """
        return reverse('view_users_profile', args=[str(self.pk)])


class Post(models.Model):
    name = models.CharField(max_length=40)
    summary = models.TextField(max_length=1000, help_text="Enter description of the post")
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(Tag, blank=True)
    publish_date = models.DateField('pubdate', default=django.utils.timezone.now, auto_now_add=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Returns the post`s url.
        """
        return reverse('post_detail', args=[str(self.pk)])

    def post_has_no_photo(self):
        return self.photo_set.count() == 0


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    text = models.TextField(max_length=1000)
    publish_date = models.DateField('pubdate', default=django.utils.timezone.now, auto_now_add=False)

    def __str__(self):
        return self.text[:75]


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Like by {self.user.username} on {self.post.name}"
