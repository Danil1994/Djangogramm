from typing import Any, Dict, List

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from main_app.forms import (CommentForm, CreatePostForm, CustomUserChangeForm,
                            CustomUserCreationForm, PhotoFormSet, TagForm)
from main_app.models import CustomUser, Photo, Post
from main_app.repositories import (CommentRepository, LikeRepository,
                                   PhotoRepository, PostCreationRepository,
                                   PostRepository, SearchRepository,
                                   SubscribeRepository)


class IndexListView(ListView):
    model = Post
    template_name = 'index.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = PostRepository.get_all_posts()
        posts_with_photos: List[Dict[str, Any]] = []

        for post in posts:
            photos = PhotoRepository.get_photos_for_post(post)
            posts_with_photos.append({'post': post, 'photos': photos})
        context["posts_with_photo"] = posts_with_photos

        posts_from_subscribe = PostRepository.get_last_posts_from_subscribe(self.request)
        posts_with_photos_from_subscribe: List[Dict[str, Any]] = []

        for post in posts_from_subscribe:
            for p in post:
                photos = PhotoRepository.get_photos_for_post(p)
                posts_with_photos_from_subscribe.append({'post': p, 'photos': photos})
        context["posts_from_subscribe"] = posts_with_photos_from_subscribe

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
        context = super().get_context_data(**kwargs)
        posts = PostRepository.get_posts_by_author(self.object)
        user = self.request.user
        subscribed_to = CustomUser.objects.get(pk=self.object.pk)

        subscribe = user.my_subscribes_dict.get(str(subscribed_to.pk))
        context['posts'] = posts
        context['subscribe'] = subscribe
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
        context.update(PostRepository.get_post_with_details(post_id))
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

        if post_form.is_valid() and photo_formset.is_valid() and tag_form.is_valid():
            post = PostCreationRepository.create_post(user=self.request.user, post_form=post_form,
                                                      photo_formset=photo_formset,
                                                      tag_form=tag_form)

            return redirect('post_detail', pk=post.pk)
        else:
            return self.render_to_response(
                self.get_context_data(post_form=post_form, photo_formset=photo_formset,
                                      tag_form=tag_form))


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

    def get(self, request: HttpRequest, post_pk: int):
        post = get_object_or_404(Post, pk=post_pk)
        form = CommentForm()
        return self.render_form(request, form, post)

    def post(self, request: HttpRequest, post_pk: int):
        post = get_object_or_404(Post, pk=post_pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            CommentRepository.add_comment(request.user, post, form.cleaned_data)
            return redirect('post_detail', pk=post.pk)
        return self.render_form(request, form, post)

    def render_form(self, request: HttpRequest, form: Any, post: int):
        return render(request, self.template_name, {'form': form, 'post': post})


class AddLikeDislike(LoginRequiredMixin, View):
    @staticmethod
    @require_POST
    def post(request: HttpRequest, pk: int):
        post = Post.objects.get(pk=pk)
        is_like = request.POST.get('is_like') == 'true'

        if is_like:
            LikeRepository.toggle_like(request, post, is_like=True)
        else:
            LikeRepository.toggle_like(request, post, is_like=False)

        likes_count = post.likes.count()
        dislikes_count = post.dislikes.count()

        return JsonResponse({'likes_count': likes_count, 'dislikes_count': dislikes_count})


class SubscribeView(LoginRequiredMixin, View):
    @staticmethod
    @require_POST
    def post(request: HttpRequest, pk: int):
        user = request.user
        subscribed_to = CustomUser.objects.get(pk=pk)
        SubscribeRepository.update_subscribe(user, subscribed_to)

        is_subscribed = SubscribeRepository.is_subscribed(user, subscribed_to)

        return JsonResponse({'is_subscribed': is_subscribed})
