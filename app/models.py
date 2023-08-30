import uuid  # Required for unique id

from django.db import models
from django.urls import reverse


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID")
    user_id = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=40)
    summary = models.TextField(max_length=1000, help_text="Enter description of the post")
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Returns the post`s url.
        """
        return reverse('post-detail', args=[str(self.id)])


class Tag(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID")
    image = models.ImageField(upload_to='static/photos/')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='photos')

    def __str__(self):
        return self.id


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID")
    name = models.CharField(max_length=20, help_text='Enter your name')
    bio = models.TextField(max_length=1000, help_text='Introduce yourself')
    avatar = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True, related_name='user_avatar')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Returns the post`s url.
        """
        return reverse('user-detail', args=[str(self.id)])


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID")
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField(max_length=1000)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        """
        Returns the post`s url.
        """
        return reverse('comment-detail', args=[str(self.id)])


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID")
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        """
        Returns the post`s url.
        """
        return reverse('comment-detail', args=[str(self.id)])
