from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailModelBackend(ModelBackend):
    """
    authentication class to login with the email address.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):

        if '@' in username:
            kwargs = {'email': username}
        else:
            return None
        if password is None:
            return None
        try:
            user = get_user_model().objects.get(**kwargs)

        except get_user_model().DoesNotExist:
            get_user_model().set_password(password)

        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user