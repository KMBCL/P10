from rest_framework.serializers import ModelSerializer

from projects.models import Comment


class CommentSerializer(ModelSerializer[Comment]):

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "issue",
            "description",
            "created_time",
        ]
        read_only_fields = [
            "id",
            "author",
            "created_time",
        ]
