from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Comment, CustomUser, Photo, Post, Tag

admin.site.register(Photo)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username", "bio", "avatar"]


admin.site.register(CustomUser, CustomUserAdmin)
