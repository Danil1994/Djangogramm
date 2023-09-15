from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Photo(models.Model):
    image = models.ImageField(upload_to='photos/', blank=True, null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.pk)


class Tag(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    bio = models.TextField(max_length=1000, help_text='Introduce yourself', default=None, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/base_avatar.png')

    def __str__(self):
        return self.username


class Post(models.Model):
    name = models.CharField(max_length=40)
    summary = models.TextField(max_length=1000, help_text="Enter description of the post")
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(Tag, blank=True)
    publish_date = models.DateField('pubdate', default=datetime.today(), auto_now_add=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Returns the post`s url.
        """
        return reverse('post_detail', args=[str(self.pk)])


class Comment(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    text = models.TextField(max_length=1000)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        """
        Returns the comment`s url.
        """
        return reverse('comment-detail', args=[str(self.pk)])


class Like(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        """
        Returns the like`s url.
        """
        return reverse('comment-detail', args=[str(self.pk)])
