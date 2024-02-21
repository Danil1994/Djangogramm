from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from main_app.forms import (CommentForm, CreatePostForm,
                            CustomUserCreationForm, TagForm,
                            validate_image_extension)
from main_app.models import CustomUser, Post


class PhotoFormTest(TestCase):

    def test_valid_image_file_extension(self):
        # Valid image extension
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        validator = validate_image_extension(image)
        self.assertIsNone(validator)

    def test_invalid_image_file_extension(self):
        # Invalid image extension
        text_file = SimpleUploadedFile("test_file.txt", b"file_content", content_type="text/plain")
        with self.assertRaises(forms.ValidationError):
            validate_image_extension(text_file)


class PostFormTest(TestCase):

    def test_valid_post_form(self):
        # Valid data
        data = {
            'name': 'Test Post',
            'summary': 'Test Summary',
        }
        form = CreatePostForm(data=data)
        self.assertTrue(form.is_valid())

    def test_empty_post_form(self):
        # Empty data? uncorrected
        data = {}
        form = CreatePostForm(data=data)
        self.assertFalse(form.is_valid())

    def test_missing_required_fields(self):
        # Missing required fields
        data = {
            'name': 'Test Post',
        }
        form = CreatePostForm(data=data)
        self.assertFalse(form.is_valid())

    def test_max_length_fields(self):
        # Check max len
        data = {
            'name': 'A' * 201,
            'summary': 'B' * 501,
        }
        form = CreatePostForm(data=data)
        self.assertFalse(form.is_valid())


class CustomUserCreationFormTest(TestCase):

    def test_valid_custom_user_creation_form(self):
        # Valid data
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'bio': 'Test Bio',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_empty_custom_user_creation_form(self):
        # Empty data, invalid
        data = {}
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_email_custom_user_creation_form(self):
        # Wrong email format, invalid
        data = {
            'username': 'testuser',
            'email': 'invalidemail',
            'bio': 'Test Bio',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_long_bio_custom_user_creation_form(self):
        # Exceeding the maximum length, Invalid
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'bio': 'B' * 1001,  # max len 1000
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())


class CommentFormTest(TestCase):

    def setUp(self):
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
        # Valid data
        data = {
            'text': 'Valid Comment Text'
        }
        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())

    def test_empty_comment_form(self):
        # Empty data, invalid
        data = {}
        form = CommentForm(data=data)
        self.assertFalse(form.is_valid())

    def test_long_comment_text(self):
        # Exceeding the maximum length, Invalid
        data = {
            'text': 'B' * 1001  # Max len 1000
        }
        form = CommentForm(data=data)
        self.assertFalse(form.is_valid())

    def test_comment_with_post(self):
        # Create comment to the post
        data = {
            'text': 'Valid Comment Text'
        }
        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())

        comment = form.save(commit=False) #connect comment with post
        comment.post = self.post
        comment.author = self.user
        comment.save()

        self.assertEqual(comment.post, self.post)


class TagFormTest(TestCase):

    def test_valid_tag_form(self):
        # Valid tag
        data = {
            'tag': 'ValidTag'
        }
        form = TagForm(data=data)
        self.assertTrue(form.is_valid())

    def test_empty_tag_form(self):
        # Empty data, invalid
        data = {}
        form = TagForm(data=data)
        self.assertFalse(form.is_valid())

    def test_long_tag_text(self):
        # Exceeding max len
        data = {
            'tag': 'B' * 101  # Max len 100
        }
        form = TagForm(data=data)
        self.assertFalse(form.is_valid())
