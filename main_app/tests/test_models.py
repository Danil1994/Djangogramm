from datetime import datetime

from django.test import TestCase

from main_app.models import Comment, CustomUser, Photo, Post, Tag


class PhotoModelTestCase(TestCase):
    def setUp(self):
        self.post = Post(name="Test Post", summary="Test summary")

    def test_photo_creation(self):
        photo = Photo(image='photos/test.jpg', post=self.post)

        self.assertIsInstance(photo, Photo)
        self.assertEqual(photo.post, self.post)


class TagModelTestCase(TestCase):
    def test_tag_creation(self):
        tag = Tag(tag="Test Tag")

        self.assertIsInstance(tag, Tag)
        self.assertEqual(tag.tag, "Test Tag")


class CustomUserModelTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser(
            username='testuser',
            password='testpassword',
            bio='This is a test bio',
            avatar='avatars/test_avatar.png'
        )

    def test_user_creation(self):
        self.assertIsInstance(self.user, CustomUser)

    def test_user_str_method(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_user_bio_field(self):
        self.assertEqual(self.user.bio, 'This is a test bio')

    def test_user_avatar_field(self):
        self.assertEqual(self.user.avatar, 'avatars/test_avatar.png')


class PostModelTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.tag = Tag.objects.create(tag='testtag')
        self.today_date = datetime.today()
        self.post = Post.objects.create(
            name='Test Post',
            summary='This is a test post summary',
            author=self.user,
            publish_date=self.today_date
        )
        self.post.tag.add(self.tag)

    def test_post_creation(self):
        self.assertIsInstance(self.post, Post)

    def test_post_name_field(self):
        self.assertEqual(self.post.name, 'Test Post')

    def test_post_summary_field(self):
        self.assertEqual(self.post.summary, 'This is a test post summary')

    def test_post_author_field(self):
        self.assertEqual(self.post.author, self.user)

    def test_post_tag_field(self):
        self.assertEqual(self.post.tag.count(), 1)

    def test_post_publish_date_field(self):
        self.assertEqual(self.post.publish_date, self.today_date)


class CommentModelTestCase(TestCase):
    def setUp(self):
        self.today_date = datetime.today()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.post = Post.objects.create(
            name='Test Post',
            summary='This is a test post summary',
            author=self.user,
            publish_date=datetime.today()
        )

        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            text='This is a test comment',
            publish_date=self.today_date
        )

    def test_comment_creation(self):
        self.assertIsInstance(self.comment, Comment)

    def test_comment_text_field(self):
        self.assertEqual(self.comment.text, 'This is a test comment')

    def test_comment_post_field(self):
        self.assertEqual(self.comment.post, self.post)

    def test_comment_user_field(self):
        self.assertEqual(self.comment.author, self.user)

    def test_comment_publish_date_field(self):
        self.assertEqual(self.comment.publish_date, self.today_date)
