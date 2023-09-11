from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from .models import User, Post, Photo, Like, Comment, Tag


def index(request):
    posts_list = Post.objects.all()
    return render(request, 'index.html', context={'posts_list': posts_list})


@login_required()
def user_profile(request):
    return render(request, 'app/user_profile.html')


@login_required()
def post_create(request):
    return render(request, 'app/post_create.html')


def explore(request):
    return render(request, 'app/explore.html')


# this best practice sou I`ll use ViewClass for all models in the future
class PostDetailView(generic.DetailView):
    model = Post
