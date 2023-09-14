from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Comment, CustomUser, Like, Photo, Post, Tag


def index(request):
    posts_list = Post.objects.all()
    return render(request, 'index.html', context={'posts_list': posts_list})


@login_required()
def user_profile(request):
    return render(request, 'main_app/user_profile.html')


@login_required()
def post_create(request):
    return render(request, 'main_app/post_create.html')


def explore(request):
    return render(request, 'main_app/explore.html')


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class EditProfile(CreateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("user_profile")
    template_name = "registration/edit_profile.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs


# this best practice sou I`ll use ViewClass for all models in the future
class PostDetailView(generic.DetailView):
    model = Post
