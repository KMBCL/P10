"""Serializers for projects."""

from rest_framework.serializers import ModelSerializer

from projects.models import Project
from authentication.serializers import UserListSerializer


class ProjectRelatedSerializer(ModelSerializer[Project]):
    """Minimal project representation for nesting in other resources."""

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
        ]
        read_only_fields = [
            "id",
        ]


class ProjectSerializer(ModelSerializer[Project]):
    """Full project representation with nested author."""

    author = UserListSerializer(read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "author",
            "name",
            "description",
            "project_type",
            "created_time",
        ]
        read_only_fields = [
            "id",
            "author",
            "created_time",
        ]
