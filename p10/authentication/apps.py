from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    # Type hérité d'AppConfig (str | _Getter[str]) : _Getter est privé aux stubs, on ne peut pas le réécrire.
    default_auto_field = 'django.db.models.BigAutoField'
    name: str = 'authentication'
