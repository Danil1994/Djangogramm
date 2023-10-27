import django

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from main_app.helping_func import photo_file_path, avatar_file_path


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
    email = models.EmailField(unique=True)  # Email field for the user (unique)
    bio = models.TextField(max_length=1000, help_text='Introduce yourself', default=None, blank=True, null=True)
    avatar = models.ImageField(upload_to=avatar_file_path, default='avatars/base_avatar.png')

    # ImageField for storing user avatars, using the avatar_file_path function for the upload_to parameter

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
    name = models.CharField(max_length=40)
    # TextField for the summary/description of the post
    summary = models.TextField(max_length=1000, help_text="Enter description of the post")
    # ForeignKey to the CustomUser model representing the author of the post
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    # Many-to-Many relationship with the Tag model, allowing multiple tags for a post (blank=True allows no tags)
    tag = models.ManyToManyField(Tag, blank=True)
    # DateField for the publish date of the post, using Django's timezone and set to the current time by defaul
    publish_date = models.DateField('pubdate', default=django.utils.timezone.now, auto_now_add=False)

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

    publish_date = models.DateField('pubdate', default=django.utils.timezone.now, auto_now_add=False)

    def __str__(self):
        return self.text[:75]


# Like model representing likes on posts
class Like(models.Model):
    # ForeignKey to the Post model, indicating the post that was liked, with CASCADE deletion behavior
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # ForeignKey to the CustomUser model representing the user who liked the post
    # SET_NULL on_delete behavior handles the deletion of related CustomUser objects, allowing likes to exist even if the user is deleted

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Like by {self.user.username} on {self.post.name}"
