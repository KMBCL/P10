from __future__ import annotations
from typing import TYPE_CHECKING, Any

from rest_framework.serializers import ModelSerializer, ValidationError

from projects.models import Comment, Issue, Project

if TYPE_CHECKING:
    from authentication.models import User


class CommentSerializer(ModelSerializer[Comment]):

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "issue",
            "description",
            "created_time",
        ]
        read_only_fields = [
            "id",
            "author",
            "created_time",
        ]

    def is_contributor(self, user: User, project: Project):
        if project is not None and not project.contributors.filter(user=user).exists():
            raise ValidationError(
                {"project": "Vous devez être contributeur du projet!"}
            )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """
        - L'utilisateur connecté doit être contributeur du projet.
        """
        issue: Issue | None = attrs.get(
            "issue", self.instance.issue if self.instance else None
        )
        if issue is None:
            raise ValidationError({"issue": "Le projet n'est pas défini."})

        project = issue.project
        user = self.context["request"].user
        self.is_contributor(user, project)
        return attrs
