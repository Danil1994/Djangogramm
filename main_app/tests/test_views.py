from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from main_app.forms import CustomUserChangeForm, CustomUserCreationForm
from main_app.models import Comment, CustomUser, Photo, Post, Tag


class PostDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_user(username='testuser', password='testpass')
        tag = Tag.objects.create(tag='tag')
        post = Post.objects.create(name='Post 1', author=user)
        Photo.objects.create(post=post, image='path/to/photo.jpg')
        post.tag.add(tag)

    def test_post_detail_view_for_logged_in_user(self):
        self.client.login(username='testuser', password='testpass')
        post = Post.objects.first()
        response = self.client.get(reverse('post_detail', args=[post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/post_detail.html')
        self.assertContains(response, 'Post 1')
        self.assertContains(response, 'path/to/photo.jpg')
        self.assertContains(response, 'tag')

    def test_post_detail_view_for_anonymous_user(self):
        post = Post.objects.first()
        response = self.client.get(reverse('post_detail', args=[post.pk]))
        self.assertEqual(response.status_code, 302)
        expected_redirect_url = '/accounts/login/?next=/main_app/post_detail/3/'
        self.assertRedirects(response, expected_redirect_url)


class CreatePostViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_create_post_view(self):
        self.client.login(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        url = reverse('post_create')

        post_data = {
            'name': 'Test Post',
            'summary': 'Test Content',
            'tag': 'tag1,tag2'
        }
        photo_data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-0-image': ''
        }
        tag_data = {
            'tag': 'tag1,tag2'
        }

        response = self.client.post(url, {**post_data, **photo_data, **tag_data})

        self.assertRedirects(response, reverse('post_detail', args=[2]))

        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().name, 'Test Post')
        self.assertEqual(Post.objects.first().summary, 'Test Content')
        self.assertEqual(Post.objects.first().author, self.user)


class IndexViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/main_app/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)

    def test_index_view_with_no_posts(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['posts_with_photo'], [])


class UserProfileTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(username='testuser', password='testpass')

    def test_user_profile_view_with_authenticated_user(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('self_profile'))
        self.assertEqual(response.status_code, 200)

    def test_user_profile_view_with_unauthenticated_user(self):
        response = self.client.get(reverse('self_profile'))
        self.assertEqual(response.status_code, 302)  # 302 is the HTTP status code for a redirect (login required)
        self.assertRedirects(response, f'/accounts/login/?next={reverse("self_profile")}')


class ExploreViewTest(TestCase):

    def test_explore_view_returns_200(self):
        response = self.client.get(reverse('explore'))
        self.assertEqual(response.status_code, 200)

    def test_explore_view_uses_correct_template(self):
        response = self.client.get(reverse('explore'))
        self.assertTemplateUsed(response, 'main_app/explore.html')


class SearchResultsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_user(username='testuser', password='testpass')
        tag1 = Tag.objects.create(tag='tag1')
        tag2 = Tag.objects.create(tag='tag2')

        post1 = Post.objects.create(name='Post 1', author=user)
        post1.tag.add(tag1)
        post2 = Post.objects.create(name='Post 2', author=user)
        post2.tag.add(tag2)
        Post.objects.create(name='Post 3', author=user)

    def test_search_results_view_with_no_query(self):
        response = self.client.get(reverse('search_view'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['posts'], [])

    def test_search_results_view_with_query(self):
        response = self.client.get(reverse('search_view') + '?q=tag1')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['posts'], ['Post 1'], transform=str)


class SignUpViewTest(TestCase):

    def test_signup_view(self):
        url = reverse('signup')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_signup_form_submission(self):
        url = reverse('signup')
        data = {
            'username': 'testuser',
            'email': 'test@mail.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        response = self.client.post(url, data)

        self.assertRedirects(response, reverse("login"))

        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.first().username, 'testuser')


class EditProfileViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(username='testuser', password='testpass')

    def test_edit_profile_view(self):
        self.client.login(username='testuser', password='testpass')

        url = reverse('edit_profile')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/edit_profile.html')

        self.assertIsInstance(response.context['form'], CustomUserChangeForm)

    def test_edit_profile_form_submission(self):
        self.client.login(username='testuser', password='testpass')

        url = reverse('edit_profile')
        data = {
            'username': 'newusername',
            'email': 'newemail@example.com'
        }

        response = self.client.post(url, data)

        self.assertRedirects(response, reverse('self_profile'))

        self.user.refresh_from_db()

        self.assertEqual(self.user.username, 'newusername')
        self.assertEqual(self.user.email, 'newemail@example.com')


class AddCommentToPostViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(username='testuser', password='testpass')
        cls.post = Post.objects.create(name='Test Post', summary='Test Content', author=cls.user)

    def test_add_comment_to_post_view_with_authenticated_user(self):
        self.client.login(username='testuser', password='testpass')

        url = reverse('add_comment_to_post', args=[self.post.pk])

        data = {'text': 'Test Comment'}
        response = self.client.post(url, data)

        self.assertRedirects(response, reverse('post_detail', args=[self.post.pk]))

        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().text, 'Test Comment')
        self.assertEqual(Comment.objects.first().post, self.post)
        self.assertEqual(Comment.objects.first().author, self.user)

    def test_add_comment_to_post_view_with_unauthenticated_user(self):
        url = reverse('add_comment_to_post', args=[self.post.pk])

        data = {'text': 'Test Comment'}
        response = self.client.post(url, data)

        self.assertRedirects(response, reverse('login') + '?next=' + url)

        self.assertEqual(Comment.objects.count(), 0)
