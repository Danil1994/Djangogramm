import uuid
from pathlib import Path
from typing import Any

from django.utils.text import slugify


def photo_file_path(instance: Any, filename: str) -> Path:
    """
    Generate the file path for uploaded photos.

    Args:
        instance (Any): The instance of the Photo model.
        filename (str): The original filename of the uploaded photo.

    Returns:
        Path: The complete file path for the uploaded photo.
    """
    author_slug: str = slugify(instance.post.author.username)
    post_name_slug: str = slugify(instance.post.name)
    unique_filename: str = f"{author_slug}--{post_name_slug}--{uuid.uuid4()}--{Path(filename).suffix}"
    return Path(f"media/photos/{unique_filename}")


def avatar_file_path(instance: object, filename: str) -> Path:
    """
    Generate the file path for user avatars.

    Args:
        instance (Type["CustomUser"]): The class type of the CustomUser model.
        filename (str): The original filename of the uploaded avatar image.

    Returns:
        Path: The complete file path for the uploaded avatar image.
    """
    username_slug: str = slugify(instance.username)
    unique_filename: str = f"{username_slug}--{uuid.uuid4()}--{Path(filename).suffix}"
    return Path(
        'https://storage.cloud.google.com/bucket-quickstart_djangogramm-399608/media/avatars/') / unique_filename
