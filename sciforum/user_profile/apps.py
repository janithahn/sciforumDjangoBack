from django.apps import AppConfig


class UserProfileConfig(AppConfig):
    name = 'user_profile'

    def ready(self):
        from .signals import log_user_logged_in_failed, log_user_logged_in_success