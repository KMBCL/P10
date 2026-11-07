from rest_framework.serializers import ModelSerializer

from projects.models import Project


class ProjectSerializer(ModelSerializer[Project]):

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
            "author",
            "created_time",
        ]
