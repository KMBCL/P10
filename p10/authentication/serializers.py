from rest_framework.serializers import ModelSerializer

from authentication.models import User


class UserSerializer(ModelSerializer[User]):

    class Meta:
        model = User
        fields = ["id", "username"]
