from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Photo(models.Model):
    image = models.ImageField(upload_to='photo', blank=True, null=True)

    def __str__(self):
        return self.pk


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
    user_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=40)
    summary = models.TextField(max_length=1000, help_text="Enter description of the post")
    tag = models.ManyToManyField('Tag')
    photos = models.ManyToManyField('Photo', related_name='posts', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Returns the post`s url.
        """
        return reverse('post-detail', args=[str(self.pk)])


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
