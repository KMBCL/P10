from rest_framework.serializers import ModelSerializer

from projects.models import Contributor


class ContributorSerializer(ModelSerializer[Contributor]):
    # unique_together (user, project) : DRF ajoute automatiquement un
    # UniqueTogetherValidator, un doublon renvoie donc une erreur 400.

    class Meta:
        model = Contributor
        fields = [
            "id",
            "user",
            "project",
            "created_time",
        ]
        read_only_fields = ["id", "created_time"]
