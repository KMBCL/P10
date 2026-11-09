from __future__ import annotations
from typing import TYPE_CHECKING, Any

from rest_framework.serializers import ModelSerializer, ValidationError

from projects.models import Contributor, Project

if TYPE_CHECKING:
    from authentication.models import User


class ContributorSerializer(ModelSerializer[Contributor]):
    # unique_together (user, project) : DRF ajoute automatiquement un
    # UniqueTogetherValidator, un doublon renvoie donc une erreur 400.

    class Meta:
        model = Contributor
        fields = [
            "id",
            "user",
            "project",
            "created_time",
        ]
        read_only_fields = ["id", "created_time"]

    def is_author(self, user: User, project: Project):
        if project is not None and project.author_id != user.id:
            raise ValidationError({"project": "Vous devez être l'auteur du projet!"})

    def validate(self, attrs: Any) -> Any:
        project = attrs.get("project", self.instance.project if self.instance else None)
        user = self.context["request"].user
        self.is_author(user, project)
        return attrs
