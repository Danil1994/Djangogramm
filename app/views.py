from django.shortcuts import render
from django.views import generic
from .models import User, Post, Photo, Like, Comment, Tag


def index(request):
    return render(request, 'index.html')


def user_profile(request):
    return render(request, 'app/user_profile.html')


def post_detail(request):
    return render(request, 'app/post_detail.html')

def post_create(request):
    return render(request, 'app/post_create.html')
