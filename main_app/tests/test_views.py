from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from main_app.forms import CustomUserChangeForm, CustomUserCreationForm
from main_app.models import Comment, CustomUser, Like, Photo, Post, Tag


class IndexViewTest(TestCase):
    def test_index_view_with_no_posts(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['posts'], [])

    def test_index_view_with_posts(self):
        Post.objects.create(name='Post 1', summary='Summary 1')
        Post.objects.create(name='Post 2', summary='Summary 2')

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        posts = response.context['posts']

        self.assertQuerysetEqual(posts, ["{'post': <Post: Post 1>, 'photos': <QuerySet []>}",
                                         "{'post': <Post: Post 2>, 'photos': <QuerySet []>}"], transform=str)


class UserProfileTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass')

    def test_user_profile_view_with_authenticated_user(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('self_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/self_profile.html')

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
        # Создаем тестовые данные для тестирования
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
        self.assertQuerysetEqual(response.context['post_list'], [])

    def test_search_results_view_with_query(self):
        response = self.client.get(reverse('search_view') + '?q=tag1')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['post_list'], ['Post 1'], transform=str)


class PostDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создаем тестовые данные для тестирования
        user = get_user_model().objects.create_user(username='testuser', password='testpass')
        tag = Tag.objects.create(tag='tag')
        post = Post.objects.create(name='Post 1', author=user)
        Photo.objects.create(post=post, image='path/to/photo.jpg')
        Like.objects.create(post=post, user=user)
        post.tag.add(tag)

    def test_post_detail_view_for_logged_in_user(self):
        self.client.login(username='testuser', password='testpass')
        post = Post.objects.first()
        response = self.client.get(reverse('post_detail', args=[post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/post_detail.html')
        self.assertContains(response, 'Post 1')  # Проверяем, что название поста отображается на странице
        self.assertContains(response, 'path/to/photo.jpg')  # Проверяем, что фотография отображается на странице
        self.assertContains(response, 'tag')  # Проверяем, что тег отображается на странице

    def test_post_detail_view_for_anonymous_user(self):
        post = Post.objects.first()
        response = self.client.get(reverse('post_detail', args=[post.pk]))
        self.assertEqual(response.status_code, 302)
        expected_redirect_url = f'/accounts/login/?next=/main_app/post/1'
        self.assertRedirects(response, expected_redirect_url)


class CreatePostViewTest(TestCase):

    def setUp(self):
        # Создаем пользователя для тестирования
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_create_post_view(self):
        # Логинимся под созданным пользователем
        self.client.login(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

        # Получаем URL для создания поста
        url = reverse('post_create')

        # Отправляем POST-запрос с корректными данными
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

        # Проверяем, что после отправки формы пользователь перенаправляется на страницу деталей поста
        self.assertRedirects(response, reverse('post_detail', args=[1]))  # Предполагается, что первый пост имеет pk=1

        # Проверяем, что пост был успешно создан в базе данных
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().name, 'Test Post')
        self.assertEqual(Post.objects.first().summary, 'Test Content')
        self.assertEqual(Post.objects.first().author, self.user)


class SignUpViewTest(TestCase):

    def test_signup_view(self):
        url = reverse('signup')
        response = self.client.get(url)

        # Проверяем, что страница существует и использует правильный шаблон
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

        # Проверяем, что форма на странице - это экземпляр CustomUserCreationForm
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

        # Проверяем, что после отправки формы пользователь перенаправляется на страницу входа
        self.assertRedirects(response, reverse("login"))

        # Проверяем, что пользователь создан в базе данных
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.first().username, 'testuser')


class EditProfileViewTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass')

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

        # Проверяем, что после отправки формы пользователь перенаправляется на страницу профиля
        self.assertRedirects(response, reverse('self_profile'))

        # Обновляем объект пользователя из базы данных
        self.user.refresh_from_db()

        # Проверяем, что данные пользователя были успешно обновлены
        self.assertEqual(self.user.username, 'newusername')
        self.assertEqual(self.user.email, 'newemail@example.com')


class AddCommentToPostViewTest(TestCase):

    def setUp(self):
        # Создаем пользователя и пост для тестирования
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(name='Test Post', summary='Test Content', author=self.user)

    def test_add_comment_to_post_view_with_authenticated_user(self):
        # Логинимся под созданным пользователем
        self.client.login(username='testuser', password='testpass')

        # Получаем URL для добавления комментария к посту
        url = reverse('add_comment_to_post', args=[self.post.pk])

        # Отправляем POST-запрос с данными комментария
        data = {'text': 'Test Comment'}
        response = self.client.post(url, data)

        # Проверяем, что после отправки формы пользователь перенаправляется на страницу деталей поста
        self.assertRedirects(response, reverse('post_detail', args=[self.post.pk]))

        # Проверяем, что комментарий был успешно добавлен к посту в базе данных
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().text, 'Test Comment')
        self.assertEqual(Comment.objects.first().post, self.post)
        self.assertEqual(Comment.objects.first().author, self.user)

    def test_add_comment_to_post_view_with_unauthenticated_user(self):
        # Не логинимся, используем анонимного пользователя

        # Получаем URL для добавления комментария к посту
        url = reverse('add_comment_to_post', args=[self.post.pk])

        # Отправляем POST-запрос с данными комментария
        data = {'text': 'Test Comment'}
        response = self.client.post(url, data)

        # Проверяем, что пользователь был перенаправлен на страницу входа
        self.assertRedirects(response, reverse('login') + '?next=' + url)

        # Проверяем, что комментарий не был добавлен к посту в базе данных
        self.assertEqual(Comment.objects.count(), 0)


class AddLikeToPostViewTest(TestCase):

    def setUp(self):
        # Создаем пользователя и пост для тестирования
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(name='Test Post', summary='Test Content', author=self.user)

    def test_add_like_to_post_view_with_authenticated_user(self):
        # Логинимся под созданным пользователем
        self.client.login(username='testuser', password='testpass')

        # Получаем URL для добавления лайка к посту
        url = reverse('add_like_to_post', args=[self.post.pk])

        # Отправляем POST-запрос для добавления лайка
        response = self.client.post(url)

        # Проверяем, что после отправки формы пользователь перенаправляется на страницу деталей поста
        self.assertRedirects(response, reverse('post_detail', args=[self.post.pk]))

        # Проверяем, что лайк был успешно добавлен к посту в базе данных
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(Like.objects.first().post, self.post)
        self.assertEqual(Like.objects.first().user, self.user)

    def test_remove_like_from_post_view_with_authenticated_user(self):
        # Создаем лайк для тестирования
        like = Like.objects.create(post=self.post, user=self.user)

        # Логинимся под созданным пользователем
        self.client.login(username='testuser', password='testpass')

        # Получаем URL для добавления/удаления лайка к посту
        url = reverse('add_like_to_post', args=[self.post.pk])

        # Отправляем POST-запрос для удаления лайка
        response = self.client.post(url)

        # Проверяем, что после отправки формы пользователь перенаправляется на страницу деталей поста
        self.assertRedirects(response, reverse('post_detail', args=[self.post.pk]))

        # Проверяем, что лайк был успешно удален из базы данных
        self.assertEqual(Like.objects.count(), 0)
