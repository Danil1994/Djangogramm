import os
import random

import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangogramm.settings")
django.setup()

from faker import Faker
from main_app.models import Comment, CustomUser, Like, Photo, Post, Tag

fake = Faker()
fake_photo_directory = os.path.join(settings.MEDIA_ROOT, 'fake_photos/')


def create_fake_tags(num_tags=10):
    for _ in range(num_tags):
        tag = Tag()
        tag.tag = fake.word()  # Генерируем случайное слово
        tag.save()
    print(f"Успешно создано {num_tags} тегов.")


def create_fake_users(num_users=10):
    for _ in range(num_users):
        user = CustomUser()
        user.username = fake.user_name()
        user.email = fake.email()
        user.password = fake.password()
        user.bio = fake.text(max_nb_chars=200)
        user.save()
    print(f"Успешно создано {num_users} юзеров.")


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
    print(f"Успешно создано {num_posts} постов.")


def create_fake_photos():
    # получаем путь к папке с фотографиями из MEDIA_ROOT
    posts = Post.objects.all()

    for post in posts:
        if post.post_has_no_photo():
            for _ in range(random.randint(1, 5)):
                # создать фейковую фотографию
                fake_photo = Photo()

                # берем случайный файл из списка фотографий
                random_photo_file = random.choice(os.listdir(fake_photo_directory))

                # полный путь к выбранному файлу в качестве изображения
                photo_path = os.path.join(fake_photo_directory, random_photo_file)

                # Связываем фейковую фотографию с выбранным постом
                fake_photo.post = post

                # Сохраняем фейковую фотографию
                fake_photo.image.save(random_photo_file, open(photo_path, 'rb'))

    print("Фейк фото успешно созданы.")


def create_fake_comments():
    posts = Post.objects.all()
    users = CustomUser.objects.all()

    for post in posts:
        num_comments = random.randint(0, 5)

        for _ in range(num_comments):
            comment = Comment()
            comment.post = post
            for _ in range(random.randint(1, 3)):
                comment.author = random.choice(users)
                comment.text = fake.paragraph(nb_sentences=3)
                comment.save()
    print("Фейк комментарии успешно созданы.")


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
    print("Фейк лайки успешно созданы.")


if __name__ == '__main__':
    create_fake_users()
    create_fake_tags()
    create_fake_posts()
    create_fake_photos()
    create_fake_comments()
    create_fake_likes()
