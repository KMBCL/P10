from __future__ import annotations

from rest_framework.serializers import ModelSerializer

from projects.models import Issue
from projects.serializers.project import ProjectRelatedSerializer
from authentication.models import User
from authentication.serializers import UserListSerializer, UserRelatedField


class AssignableUserField(UserRelatedField):
    """Seuls les contributeurs du projet de l'URL sont acceptés.

    Un id inexistant et un id hors projet tombent dans le même cas
    (does_not_exist), avec le même message : on ne révèle pas
    l'existence de comptes hors du projet (OWASP, énumération).
    """

    default_error_messages = {
        **UserRelatedField.default_error_messages,
        "does_not_exist": "Utilisateur invalide pour ce projet.",
    }

    def get_queryset(self):
        project_pk = self.context["view"].kwargs["project_pk"]
        return User.objects.filter(contributions__project_id=project_pk)


class IssueListSerializer(ModelSerializer[Issue]):
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
