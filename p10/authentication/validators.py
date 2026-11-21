from django.contrib.auth.base_user import AbstractBaseUser
from django.core.exceptions import ValidationError


class PasswordCompositionValidator:
    """Requires at least one letter, one digit and one special character."""

    def validate(self, password: str, user: AbstractBaseUser | None = None) -> None:
        """Raise ValidationError if the password lacks a letter, digit or special char."""
        has_letter: bool = any(char.isalpha() for char in password)
        has_digit: bool = any(char.isdigit() for char in password)
        has_special: bool = any(not char.isalnum() for char in password)
        if not (has_letter and has_digit and has_special):
            raise ValidationError(
                self.get_help_text(),
                code='password_composition',
            )

    def get_help_text(self) -> str:
        """Return the password composition requirement message."""
        return 'Le mot de passe doit contenir au moins une lettre, un chiffre et un caractère spécial.'
