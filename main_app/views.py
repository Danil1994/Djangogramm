from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from .forms import (CommentForm, CustomUserChangeForm, CustomUserCreationForm,
                    PhotoForm, PhotoFormSet, PostForm, TagForm)
from .models import Comment, CustomUser, Like, Photo, Post, Tag


###  GET ###
def index(request: HttpRequest) -> HttpResponse:
    posts_list = Post.objects.all().order_by('publish_date')
    return render(request, 'index.html', context={'posts_list': posts_list})


@login_required
def user_profile(request: HttpRequest) -> HttpResponse:
    return render(request, 'main_app/user_profile.html')


def explore(request: HttpRequest) -> HttpResponse:
    return render(request, 'main_app/explore.html')


class SearchResultsView(ListView):
    model = Post
    template_name = 'main_app/search_results.html'

    def get_queryset(self):

        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(name__icontains=query) | Q(tag__tag__icontains=query)
            )
        else:
            return Post.objects.none()


@login_required()
def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
    post = Post.objects.get(pk=pk)
    photos = post.photo_set.all()  # Получаем все фотографии, связанные с этим постом
    like = Like.objects.filter(post=post, user=request.user).first()
    tags = post.tag.all()

    return render(request, 'main_app/post_detail.html', {'post': post, 'photos': photos, 'like': like, 'tags': tags})


### POST ###
@login_required
def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        photo_formset = PhotoFormSet(request.POST, request.FILES, queryset=Photo.objects.none())
        tag_form = TagForm(request.POST)

        if post_form.is_valid() and photo_formset.is_valid() and tag_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()

            for photo_form in photo_formset:
                if photo_form.cleaned_data.get('image'):
                    photo = photo_form.save(commit=False)
                    photo.post = post
                    photo.save()

            tags = tag_form.cleaned_data['tag'].split(',')  # Предполагается, что теги разделяются запятыми

            for tag in tags:
                tag, created = Tag.objects.get_or_create(tag=tag.strip())
                post.tag.add(tag)

            return redirect('post_detail', pk=post.pk)

    else:
        post_form = PostForm()
        photo_formset = PhotoFormSet(queryset=Photo.objects.none())
        tag_form = TagForm()

    return render(request, 'main_app/create_post.html',
                  {'post_form': post_form,
                   'photo_formset': photo_formset,
                   'tag_form': tag_form}
                  )


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class EditProfile(UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("user_profile")
    template_name = "registration/edit_profile.html"

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def add_comment_to_post(request: HttpRequest, post_pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post_id = post.pk
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'main_app/post_detail.html', {'form': form, 'post': post})


@login_required
def add_like_to_post(request: HttpResponse, post_pk: int) -> HttpResponse:
    post = Post.objects.get(pk=post_pk)

    if request.method == 'POST':
        # Проверяем, не поставлен ли лайк уже этим пользователем
        existing_like = Like.objects.filter(post=post, user=request.user).first()

        if existing_like:
            # Лайк уже поставлен, можно реализовать отмену лайка, если нужно
            existing_like.delete()
        else:
            # Создаем и сохраняем новый лайк
            like = Like(post=post, user=request.user)
            like.save()

    return redirect('post_detail', pk=post.pk)
