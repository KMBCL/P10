from __future__ import annotations
from typing import TYPE_CHECKING, Any

from rest_framework.serializers import ModelSerializer, ValidationError

from projects.models import Comment, Contributor, Issue, Project

if TYPE_CHECKING:
    from authentication.models import User


class IssueSerializer(ModelSerializer[Issue]):

    class Meta:
        model = Issue
        fields = [
            "id",
            "author",
            "project",
            "name",
            "description",
            "status",
            "priority",
            "issue_type",
            "assigned_to",
            "created_time",
        ]
        read_only_fields = ["id", "author", "created_time"]

    def is_contributor(self, user: User, project: Project):
        if project is not None and not project.contributors.filter(user=user).exists():
            raise ValidationError(
                {"project": "Vous devez être contributeur du projet!"}
            )

    def assigned_to_is_contributor(self, assigned_to: User, project: Project):
        if (
            project is not None
            and assigned_to is not None
            and not project.contributors.filter(user=assigned_to).exists()
        ):
            raise ValidationError(
                {
                    "assigned_to": "L'utilisateur assigné doit être contributeur du projet."
                }
            )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """
        - L'utilisateur connecté doit être contributeur du projet.
        - Seuls les contributeurs du projet peuvent se voir assigner l'issue.
        """
        project = attrs.get("project", self.instance.project if self.instance else None)
        user = self.context["request"].user
        assigned_to = attrs.get(
            "assigned_to", self.instance.assigned_to if self.instance else None
        )
        self.is_contributor(user, project)
        self.assigned_to_is_contributor(assigned_to, project)
        return attrs
