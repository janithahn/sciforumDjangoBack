from django.apps import AppConfig


class AnswerConfig(AppConfig):
    name = 'answer'

    def ready(self):
        from .signals import my_handler
