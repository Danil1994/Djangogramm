from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest


class CustomEmailBackend(ModelBackend):
    def authenticate(self, request: HttpRequest, username: str = None, password: str = None, **kwargs) -> \
            Optional[get_user_model()]:
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(email=username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            pass

        return None
