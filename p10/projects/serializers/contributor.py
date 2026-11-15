from __future__ import annotations
from typing import TYPE_CHECKING

from rest_framework.serializers import ModelSerializer, ValidationError

from projects.access import AccessManager
from projects.models import Contributor

if TYPE_CHECKING:
    from authentication.models import User


class ContributorSerializer(ModelSerializer[Contributor]):

    class Meta:
        model = Contributor
        fields = [
            "id",
            "user",
            "project",
            "created_time",
        ]
        read_only_fields = ["id", "project", "created_time"]

    def validate_user(self, user: User) -> User:
        project_pk = self.context["view"].kwargs["project_pk"]
        if AccessManager(user).is_contributor(project_pk):
            raise ValidationError("Cet utilisateur est déjà contributeur du projet.")
        return user
