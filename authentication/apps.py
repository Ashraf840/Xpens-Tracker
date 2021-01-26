from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    name = 'authentication'

    # initialize the django-signals
    def ready(self):
        import authentication.signals
