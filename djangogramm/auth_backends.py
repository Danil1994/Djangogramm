from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class CustomEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs) -> Optional[get_user_model()]:
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(email=username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            pass

        return None
