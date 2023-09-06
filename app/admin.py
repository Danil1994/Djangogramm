from django.contrib import admin

from . models import Post, Photo, User, Like, Comment, Tag

admin.site.register(Photo)
admin.site.register(Post)
admin.site.register(User)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Tag)
