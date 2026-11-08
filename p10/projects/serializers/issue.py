from typing import Any

from rest_framework.serializers import ModelSerializer, ValidationError

from projects.models import Issue


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

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Seuls les contributeurs du projet peuvent se voir assigner l'issue."""
        # En modification partielle, project ou assigned_to peuvent être absents
        # de la requête : on reprend alors la valeur de l'instance existante.
        project = attrs.get("project", self.instance.project if self.instance else None)
        assigned_to = attrs.get(
            "assigned_to", self.instance.assigned_to if self.instance else None
        )

        if (
            project is not None
            and assigned_to is not None
            and not project.contributors.filter(user=assigned_to).exists()
        ):
            raise ValidationError(
                {"assigned_to": "L'utilisateur assigné doit être contributeur du projet."}
            )
        return attrs
