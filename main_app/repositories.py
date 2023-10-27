from main_app.models import Post, Photo, Like, Comment, Tag


class PostRepository:
    @staticmethod
    def get_all_posts():
        return Post.objects.all().order_by('-publish_date')

    @staticmethod
    def get_posts_by_author(author):
        return Post.objects.filter(author=author).order_by('-publish_date')

    @staticmethod
    def get_post_with_details(post_id, user):
        post = Post.objects.get(pk=post_id)
        photos = post.photo_set.all()
        like = Like.objects.filter(post=post, user=user).first()
        tags = post.tag.all()
        comments = Comment.objects.filter(post=post).order_by('-publish_date')
        return {'post': post, 'photos': photos, 'like': like, 'tags': tags, 'comments': comments}


class PostCreationRepository:
    @staticmethod
    def create_post(form, author, tag_form, photo_formset):
        post = form.save(commit=False)
        post.author = author
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
        print('post CreatE!!!!')
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


class LikeRepository:
    @staticmethod
    def toggle_like(user, post):
        existing_like = Like.objects.filter(post=post, user=user).first()
        if existing_like:
            existing_like.delete()
        else:
            like = Like(post=post, user=user)
            like.save()
