import os
import random

import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'djangogramm.settings')
django.setup()

from faker import Faker

from main_app.models import Comment, CustomUser, Photo, Post, Tag

fake = Faker()
fake_photo_directory = os.path.join(settings.MEDIA_ROOT, 'fake_photos/')

"""
Generate fake datas and save them to the database.

Args:
    num_tags (int, optional): The number of objects to generate. Defaults to 10.

Returns:
    None
"""


def create_fake_tags(num_tags: int = 10) -> None:
    for _ in range(num_tags):
        tag = Tag()
        tag.tag = fake.word()  # Generate random word
        tag.save()
    print(f"Successfully created {num_tags} tags.")


def create_fake_users(num_users: int = 10) -> None:
    for _ in range(num_users):
        username = fake.user_name()
        email = fake.email()
        password = fake.password()
        bio = fake.text(max_nb_chars=200)
        user = CustomUser(username=username, email=email, password=password, bio=bio)
        user.save()
    print(f"Successfully created {num_users} users.")


def create_fake_posts(num_posts: int = 10) -> None:
    users = CustomUser.objects.all()
    tags = Tag.objects.all()

    for _ in range(num_posts):
        post = Post()
        post.name = fake.word()
        post.summary = fake.paragraph(nb_sentences=5)
        post.author = random.choice(users)
        post.publish_date = fake.date_between(start_date='-1y', end_date='today')
        post.save()
        post.tag.set(random.sample(list(tags), random.randint(1, 3)))
    print(f"Successfully created {num_posts} posts.")


def create_fake_photos() -> None:
    posts = Post.objects.all()

    for post in posts:
        for _ in range(random.randint(1, 5)):
            # create fake photo
            fake_photo = Photo()

            # Take the random file from photo`s list
            random_photo_file = random.choice(os.listdir(fake_photo_directory))

            # Full path to the file
            photo_path = os.path.join(fake_photo_directory, random_photo_file)

            # Mounting fake photo with current post
            fake_photo.post = post

            fake_photo.image.save(random_photo_file, open(photo_path, 'rb'))

    print("Fake photo successfully created.")


def create_fake_comments() -> None:
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
    print("Fake comments successfully created.")


if __name__ == '__main__':
    create_fake_users()
    create_fake_tags()
    create_fake_posts()
    create_fake_photos()
    create_fake_comments()
