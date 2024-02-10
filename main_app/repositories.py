import datetime

from django.contrib.auth.decorators import login_required
from django.utils import timezone

from main_app.models import Comment, CustomUser, Photo, Post, Tag


class LikeRepository:
    @staticmethod
    def toggle_like(request, post, is_like):
        likes_set = post.likes.all()
        dislikes_set = post.dislikes.all()

        if is_like:
            if request.user in likes_set:
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)
                post.dislikes.remove(request.user)
        else:
            if request.user in dislikes_set:
                post.dislikes.remove(request.user)
            else:
                post.dislikes.add(request.user)
                post.likes.remove(request.user)


class SubscribeRepository:
    @staticmethod
    def is_subscribed(user, subscribed_to):
        return bool(user.my_subscribes_dict.get(str(subscribed_to.pk)))

    @staticmethod
    def update_subscribe(user, subscribed_to):
        if user.my_subscribes_dict.get(str(subscribed_to.pk)):
            del user.my_subscribes_dict[str(subscribed_to.pk)]
        else:
            user.my_subscribes_dict[str(subscribed_to.pk)] = subscribed_to.username
        user.save()


class PostRepository:
    @staticmethod
    @login_required
    def get_last_posts_from_subscribe(request):
        user = request.user
        last_posts_from_subscribe_list = []
        one_day_ago = timezone.now() - datetime.timedelta(days=1)

        for sub in user.my_subscribes_dict:
            user = CustomUser.objects.get(pk=sub)
            posts = user.posts.filter(publish_date__gte=one_day_ago)
            last_posts_from_subscribe_list.append(posts)

        return last_posts_from_subscribe_list

    @staticmethod
    def get_all_posts():
        return Post.objects.all().order_by('-publish_date')

    @staticmethod
    def get_posts_by_author(author):
        return Post.objects.filter(author=author).order_by('-publish_date')

    @staticmethod
    def get_post_with_details(post_id):
        post = Post.objects.get(pk=post_id)
        photos = post.photo_set.all()
        tags = post.tag.all()
        comments = Comment.objects.filter(post=post).order_by('-publish_date')
        return {'post': post, 'photos': photos, 'tags': tags, 'comments': comments}


class PostCreationRepository:
    @staticmethod
    def create_post(user, post_form, photo_formset, tag_form):
        post = post_form.save(commit=False)
        post.author = user
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
        return post


class PhotoRepository:
    @staticmethod
    def get_photos_for_post(post):
        return Photo.objects.filter(post=post)


class SearchRepository:
    @staticmethod
    def search_posts(query):
        name_filtered = Post.objects.filter(name__icontains=query)
        tag_filtered = Post.objects.filter(tag__tag__icontains=query)
        return name_filtered.union(tag_filtered)


class CommentRepository:
    @staticmethod
    def add_comment(user, post, form_data):
        comment = Comment(author=user, post=post, **form_data)
        comment.save()
        return comment
