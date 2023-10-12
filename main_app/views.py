from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from main_app.forms import (CommentForm, CustomUserChangeForm,
                            CustomUserCreationForm, PhotoFormSet, PostForm,
                            TagForm)
from main_app.models import CustomUser, Like, Photo, Post, Tag


#  GET ###
def index(request):
    posts_list = Post.objects.all().order_by('publish_date')
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    # Получите фотографии для каждого поста и добавьте их в контекст
    posts_with_photos = []
    for post in posts:
        photos = Photo.objects.filter(post=post)
        posts_with_photos.append({'post': post, 'photos': photos})

    context = {
        'posts': posts_with_photos
    }
    return render(request, 'index.html', context)


@login_required
def user_profile(request: HttpRequest) -> HttpResponse:
    user = request.user  # Получаем текущего пользователя
    posts = Post.objects.filter(author=user)  # Получаем все посты пользователя
    return render(request, 'main_app/self_profile.html', {'user': user, 'posts': posts})


def view_users_profile(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    posts = Post.objects.filter(author=user)
    return render(request, 'main_app/view_users_profile.html', {'other_user': user, 'posts': posts})


def explore(request: HttpRequest) -> HttpResponse:
    return render(request, 'main_app/explore.html')


class SearchResultsView(ListView):
    model = Post
    template_name = 'main_app/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            # distinct() для удаления дубликатов
            return Post.objects.filter(
                Q(name__icontains=query) | Q(tag__tag__icontains=query)
            ).distinct()
        else:
            return Post.objects.none()


@login_required()
def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
    post = Post.objects.get(pk=pk)
    photos = post.photo_set.all()  # Получаем все фотографии, связанные с этим постом
    like = Like.objects.filter(post=post, user=request.user).first()
    tags = post.tag.all()

    return render(request, 'main_app/post_detail.html', {'post': post, 'photos': photos, 'like': like, 'tags': tags})


# POST ###
@login_required
def create_post(request: HttpRequest):
    post_form = PostForm()
    photo_formset = PhotoFormSet(queryset=Photo.objects.none())
    tag_form = TagForm()

    if request.method == 'POST':
        post_form = PostForm(request.POST)
        photo_formset = PhotoFormSet(request.POST, request.FILES, queryset=Photo.objects.none())
        tag_form = TagForm(request.POST)

        if post_form.is_valid() and photo_formset.is_valid() and tag_form.is_valid():
            # create post
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            # add all photo to post
            for photo_form in photo_formset:
                if photo_form.cleaned_data.get('image'):
                    photo = photo_form.save(commit=False)
                    photo.post = post
                    photo.save()
            # split tags and add them to post
            tags = tag_form.cleaned_data['tag'].split(',')

            for tag in tags:
                tag, created = Tag.objects.get_or_create(tag=tag.strip())
                post.tag.add(tag)

            messages.success(request, 'Пост успешно создан.')  # Уведомление об успешном создании поста
            return redirect('post_detail', pk=post.pk)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
            print(f'Post errors: {post_form.errors}',
                  f'Tag errors: {tag_form.errors}',
                  f'Photo errors:{photo_formset.errors}'
                  )

    return render(request, 'main_app/create_post.html',
                  {'post_form': post_form,
                   'photo_formset': photo_formset,
                   'tag_form': tag_form}
                  )


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_invalid(self, form):
        # Получаем сообщения об ошибках из формы
        error_messages = form.errors
        # Передаем сообщения об ошибках в контекст шаблона
        return self.render_to_response(self.get_context_data(form=form, error_messages=error_messages))


class EditProfile(UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("self_profile")
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
            # Лайк уже поставлен, можно сделать отмену лайка, если нужно
            existing_like.delete()
        else:
            # Создаем и сохраняем новый лайк
            like = Like(post=post, user=request.user)
            like.save()

    return redirect('post_detail', pk=post.pk)
