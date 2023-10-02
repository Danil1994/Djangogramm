import os
import random

import django
from dotenv import load_dotenv

load_dotenv()
photo_folder = os.getenv('photo_folder')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangogramm.settings")
django.setup()

from faker import Faker

from main_app.models import Comment, CustomUser, Like, Photo, Post, Tag

fake = Faker()


def create_fake_tags(num_tags=10):
    for _ in range(num_tags):
        tag = Tag()
        tag.tag = fake.word()  # Генерируем случайное слово
        tag.save()


def create_fake_users(num_users=10):
    for _ in range(num_users):
        user = CustomUser()
        user.username = fake.user_name()
        user.email = fake.email()
        user.password = fake.password()
        user.bio = fake.text(max_nb_chars=200)
        user.save()


def create_fake_posts(num_posts=10):
    users = CustomUser.objects.all()
    tags = Tag.objects.all()

    for _ in range(num_posts):
        post = Post()
        post.name = fake.sentence(nb_words=6)
        post.summary = fake.paragraph(nb_sentences=5)
        post.author = random.choice(users)
        post.publish_date = fake.date_between(start_date='-1y', end_date='today')
        post.save()
        post.tag.set(random.sample(list(tags), random.randint(1, 3)))


def create_fake_photos():
    # список файлов из папки с фотографиями

    photo_files = [os.path.join(photo_folder, filename) for filename in os.listdir(photo_folder) if
                   os.path.isfile(os.path.join(photo_folder, filename))]

    posts = Post.objects.all()

    for post in posts:
        while post.has_less_than_five_photos():

            for _ in range(random.randint(1, 5)):
                # создать фейковую фотографию
                fake_photo = Photo()

                # берем случайный файл из списка фотографий
                random_photo_file = random.choice(photo_files)

                # путь к выбранному файлу в качестве изображения
                fake_photo.image = random_photo_file

                # Связываем фейковую фотографию с выбранным постом
                fake_photo.post = post

                # Сохраняем фейковую фотографию
                fake_photo.save()


def create_fake_comments():
    posts = Post.objects.all()
    users = CustomUser.objects.all()

    for post in posts:
        num_comments = random.randint(0, 5)

        for _ in range(num_comments):
            comment = Comment()
            comment.post = post
            for _ in range(random.randint(1, 3)):
                comment.user = random.choice(users)
                comment.text = fake.paragraph(nb_sentences=3)
                comment.save()


def create_fake_likes():
    posts = Post.objects.all()
    users = CustomUser.objects.all()

    for post in posts:
        num_likes = random.randint(0, 10)  # Генерируем случайное количество лайков для данного поста

        for _ in range(num_likes):
            like = Like()
            like.post = post
            like.user = random.choice(users)
            like.save()


if __name__ == '__main__':
    create_fake_users()
    create_fake_tags()
    create_fake_posts()
    create_fake_photos()
    create_fake_comments()
    create_fake_likes()
