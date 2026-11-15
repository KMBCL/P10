from rest_framework.serializers import ModelSerializer

from projects.models import Project
from authentication.serializers import UserListSerializer


class ProjectRelatedSerializer(ModelSerializer[Project]):
    author = UserListSerializer(read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "author",
            "name",
        ]
        read_only_fields = [
            "id",
            "author",
        ]


class ProjectSerializer(ModelSerializer[Project]):
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
