from typing import Any

from rest_framework.serializers import ModelSerializer


from authentication.models import User


class UserSerializer(ModelSerializer[User]):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict[str, Any]) -> User:
        return User.objects.create_user(**validated_data)
