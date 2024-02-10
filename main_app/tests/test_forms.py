from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from main_app.forms import (CommentForm, CreatePostForm,
                            CustomUserCreationForm, TagForm,
                            validate_image_extension)
from main_app.models import CustomUser, Post


class PhotoFormTest(TestCase):

    def test_valid_image_file_extension(self):
        # Правильное расширение файла (.jpg), валидатор не должен вызывать ошибок
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        validator = validate_image_extension(image)
        self.assertIsNone(validator)  # Проверяем, что валидатор не вызывает ошибок

    def test_invalid_image_file_extension(self):
        # Неправильное расширение файла (.txt), валидатор должен вызвать ошибку
        text_file = SimpleUploadedFile("test_file.txt", b"file_content", content_type="text/plain")
        with self.assertRaises(forms.ValidationError):
            validate_image_extension(text_file)  # Проверяем, что валидатор вызывает ошибку


class PostFormTest(TestCase):

    def test_valid_post_form(self):
        # Валидные данные формы, форма должна быть валидной
        data = {
            'name': 'Test Post',
            'summary': 'Test Summary',
        }
        form = CreatePostForm(data=data)
        self.assertTrue(form.is_valid())  # Проверяем, что форма считается валидной с корректными данными

    def test_empty_post_form(self):
        # Пустые данные, форма должна быть невалидной
        data = {}
        form = CreatePostForm(data=data)
        self.assertFalse(form.is_valid())  # Проверяем, что форма считается невалидной с пустыми данными

    def test_missing_required_fields(self):
        # Недостающие обязательные поля, форма должна быть невалидной
        data = {
            'name': 'Test Post',
        }
        form = CreatePostForm(data=data)
        self.assertFalse(form.is_valid())  # Проверяем, что форма считается невалидной без всех обязательных полей

    def test_max_length_fields(self):
        # Проверяем максимальную длину полей name и summary
        data = {
            'name': 'A' * 201,  # Превышаем максимальную длину 200 символов
            'summary': 'B' * 501,  # Превышаем максимальную длину 500 символов
        }
        form = CreatePostForm(data=data)
        self.assertFalse(form.is_valid())  # Проверяем, что форма считается невалидной


class CustomUserCreationFormTest(TestCase):

    def test_valid_custom_user_creation_form(self):
        # Валидные данные формы, форма должна быть валидной
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'bio': 'Test Bio',
            'password1': 'testpassword123',  # Пароль
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=data)
        self.assertTrue(form.is_valid())  # Проверяем, что форма считается валидной с корректными данными

    def test_empty_custom_user_creation_form(self):
        # Пустые данные, форма должна быть невалидной
        data = {}
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())  # Проверяем, что форма считается невалидной с пустыми данными

    def test_invalid_email_custom_user_creation_form(self):
        # Неверный формат email, форма должна быть невалидной
        data = {
            'username': 'testuser',
            'email': 'invalidemail',  # Неверный формат email
            'bio': 'Test Bio',
            'password1': 'testpassword123',  # Пароль
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())  # Проверяем, что форма считается невалидной с неверным email

    def test_long_bio_custom_user_creation_form(self):
        # Превышение максимальной длины поля bio, форма должна быть невалидной
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'bio': 'B' * 1001,  # Превышаем максимальную длину 1000 символов
            'password1': 'testpassword123',  # Пароль
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())  # Проверяем, что форма считается невалидной


class CommentFormTest(TestCase):

    def setUp(self):
        # Создаем пользователя и пост, чтобы использовать в тестах
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )
        self.post = Post.objects.create(
            name='Test Post',
            summary='Test Summary',
            author=self.user
        )

    def test_valid_comment_form(self):
        # Валидные данные формы, форма должна быть валидной
        data = {
            'text': 'Valid Comment Text'
        }
        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())  # Проверяем, что форма считается валидной с корректными данными

    def test_empty_comment_form(self):
        # Пустые данные, форма должна быть невалидной
        data = {}
        form = CommentForm(data=data)
        self.assertFalse(form.is_valid())  # Проверяем, что форма считается невалидной с пустыми данными

    def test_long_comment_text(self):
        # Превышение максимальной длины текста комментария, форма должна быть невалидной
        data = {
            'text': 'B' * 1001  # Превышаем максимальную длину 1000 символов
        }
        form = CommentForm(data=data)
        self.assertFalse(form.is_valid())  # Проверяем, что форма считается невалидной

    def test_comment_with_post(self):
        # Создаем комментарий, связанный с постом
        data = {
            'text': 'Valid Comment Text'
        }
        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())  # Проверяем, что форма считается валидной

        comment = form.save(commit=False)
        comment.post = self.post  # Присваиваем комментарию связанный пост
        comment.author = self.user
        comment.save()

        self.assertEqual(comment.post, self.post)  # Проверяем, что комментарий связан с правильным постом


class TagFormTest(TestCase):

    def test_valid_tag_form(self):
        # Валидные данные формы, форма должна быть валидной
        data = {
            'tag': 'ValidTag'
        }
        form = TagForm(data=data)
        self.assertTrue(form.is_valid())  # Проверяем, что форма считается валидной с корректными данными

    def test_empty_tag_form(self):
        # Пустые данные, форма должна быть невалидной
        data = {}
        form = TagForm(data=data)
        self.assertFalse(form.is_valid())  # Проверяем, что форма считается невалидной с пустыми данными

    def test_long_tag_text(self):
        # Превышение максимальной длины текста тега, форма должна быть невалидной
        data = {
            'tag': 'B' * 101  # Превышаем максимальную длину 100 символов
        }
        form = TagForm(data=data)
        self.assertFalse(form.is_valid())  # Проверяем, что форма считается невалидной
