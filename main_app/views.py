from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import (CustomUserChangeForm, CustomUserCreationForm, PhotoForm,
                    PostForm)
from .models import Comment, CustomUser, Like, Photo, Post, Tag


def index(request):
    posts_list = Post.objects.all()
    return render(request, 'index.html', context={'posts_list': posts_list})


@login_required()
def user_profile(request):
    return render(request, 'main_app/user_profile.html')


def explore(request):
    return render(request, 'main_app/explore.html')


@login_required()
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    photos = post.photo_set.all()  # Получаем все фотографии, связанные с этим постом
    return render(request, 'main_app/post_detail.html', {'post': post, 'photos': photos})


@login_required()
def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        photo_form = PhotoForm(request.POST, request.FILES)  # request.FILES для обработки загрузки файлов

        if post_form.is_valid() and photo_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()

            photo = photo_form.save(commit=False)
            photo.post = post  # Привязываем фото к посту
            photo.save()

            return redirect('post_detail', pk=post.pk)

    else:
        post_form = PostForm()
        photo_form = PhotoForm()

    return render(request, 'main_app/create_post.html', {'post_form': post_form, 'photo_form': photo_form})


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class EditProfile(CreateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("user_profile")
    template_name = "registration/edit_profile.html"

    def get_form_kwargs(self):  # получаем имя юзера и сохраняем как автора
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs
