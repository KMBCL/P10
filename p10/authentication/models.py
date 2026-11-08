from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.expressions import Combinable

from authentication.constants import MIN_ALLOWED_AGE


class User(AbstractUser):
    """Utilisateur SoftDesk : identifiants natifs + âge et consentements RGPD."""

    username: models.CharField[str | int | Combinable, str] = models.CharField(
        max_length=50,
        unique=True,
        validators=[UnicodeUsernameValidator()],
    )
    # RGPD : inscription interdite aux 15 ans et moins.
    age: models.PositiveIntegerField[int | Combinable, int] = (
        models.PositiveIntegerField(
            validators=[MinValueValidator(MIN_ALLOWED_AGE)],
        )
    )
    # Consentements explicites : False tant que l'utilisateur ne les donne pas.
    can_be_contacted: models.BooleanField[bool | Combinable, bool] = (
        models.BooleanField(default=False)
    )
    can_data_be_shared: models.BooleanField[bool | Combinable, bool] = (
        models.BooleanField(default=False)
    )

    # Demandés par createsuperuser : age n'a pas de valeur par défaut.
    REQUIRED_FIELDS: ClassVar[list[str]] = ["email", "age"]
