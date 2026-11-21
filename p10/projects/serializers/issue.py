from __future__ import annotations

from rest_framework.serializers import ModelSerializer

from projects.models import Issue
from projects.serializers.project import ProjectRelatedSerializer
from authentication.models import User
from authentication.serializers import UserListSerializer, UserRelatedField


class AssignableUserField(UserRelatedField):
    """Accepts only project contributors, with one error message to prevent user enumeration."""

    default_error_messages = {
        **UserRelatedField.default_error_messages,
        "does_not_exist": "Utilisateur invalide pour ce projet.",
    }

    def get_queryset(self):
        project_pk = self.context["view"].kwargs["project_pk"]
        return User.objects.filter(contributions__project_id=project_pk)


class IssueListSerializer(ModelSerializer[Issue]):
    """Lightweight issue representation for list views."""

    author = UserListSerializer(read_only=True)
    assigned_to = UserListSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = [
            "id",
            "author",
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
    """Full issue representation with nested author and project."""

    author = UserListSerializer(read_only=True)
    project = ProjectRelatedSerializer(read_only=True)
    assigned_to = AssignableUserField(allow_null=True, required=False)

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
