from __future__ import annotations
from typing import TYPE_CHECKING

from rest_framework.serializers import ModelSerializer, ValidationError

from projects.models import Contributor, Issue
from projects.serializers.project import ProjectRelatedSerializer
from authentication.serializers import UserListSerializer

if TYPE_CHECKING:
    from authentication.models import User


class IssueListSerializer(ModelSerializer[Issue]):
    author = UserListSerializer(read_only=True)
    project = ProjectRelatedSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = [
            "id",
            "author",
            "project",
            "name",
            "status",
            "priority",
            "issue_type",
            "assigned_to",
        ]
        read_only_fields = [
            "id",
        ]


class IssueSerializer(ModelSerializer[Issue]):
    author = UserListSerializer(read_only=True)
    # Le projet vient de l'URL (perform_create), jamais du body.
    project = ProjectRelatedSerializer(read_only=True)

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

    def validate_assigned_to(self, assigned_to: User | None) -> User | None:
        project_pk = self.context["view"].kwargs["project_pk"]
        if (
            assigned_to is not None
            and not Contributor.objects.filter(
                project_id=project_pk, user=assigned_to
            ).exists()
        ):
            raise ValidationError(
                "L'utilisateur assigné doit être contributeur du projet."
            )
        return assigned_to
