import django
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from main_app.helping_func import avatar_file_path, photo_file_path


# Photo model representing uploaded images
class Photo(models.Model):
    image = models.ImageField(upload_to=photo_file_path, blank=True, null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.pk)


# Tag model representing tags associated with posts
class Tag(models.Model):
    tag = models.CharField(max_length=50, primary_key=True, help_text="Enter tags separated by commas")

    def __str__(self):
        return self.tag


# Custom user model extending the AbstractUser class
class CustomUser(AbstractUser):
    # Email field for the user (unique)
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=1000, help_text='Introduce yourself', default=None, blank=True, null=True)
    # ImageField for storing user avatars, using the avatar_file_path function for the upload_to parameter
    avatar = models.ImageField(upload_to=avatar_file_path, default='avatars/base_avatar.png')
    my_subscribes_dict = models.JSONField(default=dict)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        """
        Returns the post`s url.
        """
        return reverse('someone_profile', args=[str(self.pk)])


# Post model representing individual posts
class Post(models.Model):
    # CharField for the name of the post
    name = models.CharField(max_length=50)
    # TextField for the summary/description of the post
    summary = models.TextField(max_length=1000, help_text="Enter description of the post")
    # ForeignKey to the CustomUser model representing the author of the post
    author = models.ForeignKey(CustomUser, related_name='posts', on_delete=models.SET_NULL, null=True)
    # Many-to-Many relationship with the Tag model, allowing multiple tags for a post (blank=True allows no tags)
    tag = models.ManyToManyField(Tag, blank=True)
    # DateField for the publish date of the post, using Django's timezone and set to the current time by defaul
    publish_date = models.DateTimeField('pubdate', default=django.utils.timezone.now, auto_now_add=False)

    likes = models.ManyToManyField(CustomUser, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(CustomUser, blank=True, related_name='dislikes')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Returns the post`s url.
        """
        return reverse('post_detail', args=[str(self.pk)])


# Comment model representing comments on posts
class Comment(models.Model):
    # ForeignKey to the Post model, indicating the post to which the comment belongs
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # ForeignKey to the CustomUser model representing the author of the comment
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    # TextField for the text of the comment
    text = models.TextField(max_length=1000)
    # DateField for the publish date of the comment, using Django's timezone and set to the current time by default

    publish_date = models.DateTimeField('pubdate', default=django.utils.timezone.now, auto_now_add=False)

    def __str__(self):
        return self.text[:75]
