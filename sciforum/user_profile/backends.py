from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


class EmailModelBackend(ModelBackend):
    """
    authentication class to login with the email address.
    """

    '''def authenticate(self, request, username=None, password=None, **kwargs):

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
                return user'''

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = get_user_model().objects.get(
                Q(username__iexact=username) | Q(email__iexact=username))
        except get_user_model().DoesNotExist:
            return None
        except Exception as excep:
            return get_user_model().objects.filter(email=username).order_by('id').first()
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None