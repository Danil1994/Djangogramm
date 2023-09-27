from django.test import TestCase
from django.urls import reverse

from main_app.models import CustomUser, Post


class IndexViewTest(TestCase):
    def test_index_view_with_no_posts(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['posts_list'], [])

    def test_index_view_with_posts(self):
        Post.objects.create(name='Post 1', summary='Summary 1')
        Post.objects.create(name='Post 2', summary='Summary 2')

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        posts = response.context['posts_list']
        post_strings = [str(post) for post in posts]

        self.assertQuerysetEqual(post_strings, ['Post 1', 'Post 2'])
