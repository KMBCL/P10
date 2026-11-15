from rest_framework.serializers import ModelSerializer

from projects.models import Comment
from authentication.serializers import UserListSerializer


class CommentSerializer(ModelSerializer[Comment]):
    author = UserListSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "issue",
            "description",
            "created_time",
        ]
        # L'issue vient de l'URL (perform_create), jamais du body.
        read_only_fields = [
            "id",
            "author",
            "issue",
            "created_time",
        ]
