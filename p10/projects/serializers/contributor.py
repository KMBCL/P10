from __future__ import annotations

from rest_framework.serializers import ModelSerializer, ValidationError

from authentication.models import User
from authentication.serializers import UserRelatedField
from projects.access import AccessManager
from projects.models import Contributor


class ContributorSerializer(ModelSerializer[Contributor]):
    """Contributor representation; rejects users already in the project."""

    user = UserRelatedField(queryset=User.objects.all())

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
