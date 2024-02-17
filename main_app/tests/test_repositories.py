from django.test import RequestFactory, TestCase

from main_app.models import CustomUser, Post
from main_app.repositories import LikeRepository


class LikeRepositoryTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username='test_user',
            password='test_password'
        )
        self.post = Post.objects.create(
            name='Test Post',
            summary='Test Content',
            author=self.user
        )
        self.request = RequestFactory().post('/some-url/')
        self.request.user = self.user

    def test_toggle_like_add_like(self):
        # Initial state: No likes or dislikes
        self.assertEqual(self.post.likes.count(), 0)
        self.assertEqual(self.post.dislikes.count(), 0)

        # Toggle like: add a like
        LikeRepository.toggle_like(request=self.request, post=self.post, is_like=True)

        # Check the result
        self.assertEqual(self.post.likes.count(), 1)
        self.assertEqual(self.post.dislikes.count(), 0)

    def test_toggle_like_remove_like(self):
        # Initial state: Add a like
        self.post.likes.add(self.user)
        self.assertEqual(self.post.likes.count(), 1)
        self.assertEqual(self.post.dislikes.count(), 0)

        # Toggle like: remove the like
        LikeRepository.toggle_like(request=self.request, post=self.post, is_like=True)

        # Check the result
        self.assertEqual(self.post.likes.count(), 0)
        self.assertEqual(self.post.dislikes.count(), 0)

    def test_toggle_like_add_dislike(self):
        # Initial state: No likes or dislikes
        self.assertEqual(self.post.likes.count(), 0)
        self.assertEqual(self.post.dislikes.count(), 0)

        # Toggle like: add a dislike
        LikeRepository.toggle_like(request=self.request, post=self.post, is_like=False)

        # Check the result
        self.assertEqual(self.post.likes.count(), 0)
        self.assertEqual(self.post.dislikes.count(), 1)

    def test_toggle_like_remove_dislike(self):
        # Initial state: Add a dislike
        self.post.dislikes.add(self.user)
        self.assertEqual(self.post.likes.count(), 0)
        self.assertEqual(self.post.dislikes.count(), 1)

        # Toggle like: remove the dislike
        LikeRepository.toggle_like(request=self.request, post=self.post, is_like=False)

        # Check the result
        self.assertEqual(self.post.likes.count(), 0)
        self.assertEqual(self.post.dislikes.count(), 0)
