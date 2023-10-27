from typing import Any, Dict, List

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from main_app.forms import (CommentForm, CustomUserChangeForm,
                            CustomUserCreationForm, PhotoFormSet, CreatePostForm,
                            TagForm)
from main_app.models import CustomUser, Like, Photo, Post, Tag, Comment
from main_app.repositories import (CommentRepository,
                                   LikeRepository,
                                   PostCreationRepository,
                                   PostRepository,
                                   PhotoRepository,
                                   SearchRepository)


class IndexView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self) -> List[Post]:
        return PostRepository.get_all_posts()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        posts_with_photos: List[Dict[str, Any]] = []

        for post in context['posts']:
            photos = PhotoRepository.get_photos_for_post(post)
            posts_with_photos.append({'post': post, 'photos': photos})

        context['posts'] = posts_with_photos
        return context


class SelfProfileView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'main_app/self_profile.html'
    context_object_name = 'posts'

    def get_queryset(self) -> List[Post]:
        return PostRepository.get_posts_by_author(self.request.user)


class SomeoneProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'main_app/someone_profile.html'
    context_object_name = 'other_user'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        print('blabla')
        context = super().get_context_data(**kwargs)
        posts = PostRepository.get_posts_by_author(self.object)
        context['posts'] = posts
        return context


class ExploreView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'main_app/explore.html')


class SearchResultsView(ListView):
    model = Post
    template_name = 'main_app/search_results.html'
    context_object_name = 'posts'

    def get_queryset(self) -> List[Post]:
        query = self.request.GET.get('q')
        if query:
            return SearchRepository.search_posts(query)
        return Post.objects.none()


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'main_app/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.object.pk
        user = self.request.user
        context.update(PostRepository.get_post_with_details(post_id, user))
        return context




class CreatePostView(LoginRequiredMixin, CreateView):
    template_name = 'main_app/create_post.html'
    form_class = CreatePostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['post_form'] = self.form_class(self.request.POST)
            context['photo_formset'] = PhotoFormSet(self.request.POST, self.request.FILES)
            context['tag_form'] = TagForm(self.request.POST)
        else:
            context['post_form'] = self.form_class()
            context['photo_formset'] = PhotoFormSet(queryset=Photo.objects.none())
            context['tag_form'] = TagForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        post_form = context['post_form']
        photo_formset = context['photo_formset']
        tag_form = context['tag_form']

        if form.is_valid() and photo_formset.is_valid() and tag_form.is_valid():
            post = form.save(commit=False)
            post.author = self.request.user
            post.save()

            for photo_form in photo_formset:
                if photo_form.cleaned_data.get('image'):
                    photo = photo_form.save(commit=False)
                    photo.post = post
                    photo.save()

            tags = tag_form.cleaned_data['tag'].split(',')
            for tag in tags:
                tag, created = Tag.objects.get_or_create(tag=tag.strip())
                post.tag.add(tag)

            return redirect('post_detail', pk=post.pk)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, post_form=post_form, photo_formset=photo_formset,
                                      tag_form=tag_form))


# class CreatePostView(LoginRequiredMixin, View):
#     template_name = 'main_app/create_post.html'
#     form_class = CreatePostForm
#
#     def get(self, request):
#         post_form = self.form_class()
#         photo_formset = PhotoFormSet(queryset=Photo.objects.none())
#         tag_form = TagForm()
#         return render(request, self.template_name,
#                       {'post_form': post_form, 'photo_formset': photo_formset, 'tag_form': tag_form})
#
#     def post(self, request):
#         post_form = self.form_class(request.POST)
#         photo_formset = PhotoFormSet(request.POST, request.FILES)
#         tag_form = TagForm(request.POST)
#
#         if post_form.is_valid() and photo_formset.is_valid() and tag_form.is_valid():
#             name = post_form.cleaned_data['name']
#             summary = post_form.cleaned_data['summary']
#             tags = tag_form.cleaned_data['tag']
#             photos = [form.cleaned_data['image'] for form in photo_formset if form.cleaned_data.get('image')]
#             post = PostCreationRepository.create_post(request.user, name, summary, tags, photos)
#             return redirect('post_detail', pk=post.pk)
#         else:
#             print('no create')
#             return render(request, self.template_name,
#                           {'post_form': post_form, 'photo_formset': photo_formset, 'tag_form': tag_form})
#

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_invalid(self, form):
        error_messages = form.errors
        return self.render_to_response(self.get_context_data(form=form, error_messages=error_messages))


class EditProfile(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("self_profile")
    template_name = "registration/edit_profile.html"

    def get_object(self, queryset=None):
        return self.request.user


class AddCommentToPostView(LoginRequiredMixin, View):
    template_name = 'main_app/post_detail.html'

    def get(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        form = CommentForm()
        return self.render_form(request, form, post)

    def post(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            CommentRepository.add_comment(request.user, post, form.cleaned_data)
            return redirect('post_detail', pk=post.pk)
        return self.render_form(request, form, post)

    def render_form(self, request, form, post):
        return render(request, self.template_name, {'form': form, 'post': post})


class AddLikeToPostView(LoginRequiredMixin, View):
    def post(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        LikeRepository.toggle_like(request.user, post)
        return redirect('post_detail', pk=post.pk)
