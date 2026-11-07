from django.contrib.auth.base_user import AbstractBaseUser
from django.core.exceptions import ValidationError


class PasswordCompositionValidator:
    """Exige au moins une lettre, un chiffre et un caractère spécial.

    Django ne fournit pas ce contrôle nativement ; la longueur reste gérée par MinimumLengthValidator.
    """

    def validate(self, password: str, user: AbstractBaseUser | None = None) -> None:
        has_letter: bool = any(char.isalpha() for char in password)
        has_digit: bool = any(char.isdigit() for char in password)
        has_special: bool = any(not char.isalnum() for char in password)
        if not (has_letter and has_digit and has_special):
            raise ValidationError(
                self.get_help_text(),
                code='password_composition',
            )

    def get_help_text(self) -> str:
        return 'Le mot de passe doit contenir au moins une lettre, un chiffre et un caractère spécial.'
