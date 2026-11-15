from typing import Any

from rest_framework.serializers import (
    ModelSerializer,
    ValidationError as SerializerValidationError,
)
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as CoreValidationError


from authentication.models import User


class UserListSerializer(ModelSerializer[User]):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
        ]
        read_only_fields = fields


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

    def temp_user(self, attrs: Any) -> User:
        """Creates temp user created for UserAttributeSimilarityValidator."""
        user = User(**{key: value for key, value in attrs.items() if key != "password"})
        return user

    def validate(self, attrs: Any) -> Any:
        """Valides user data.

        temp_user is used for create action
        otherwise self.instance is used
        """
        password = attrs.get("password")
        if password is not None:
            user = self.instance or self.temp_user(attrs)

            try:
                validate_password(attrs["password"], user=user)
            except CoreValidationError as exception:
                raise SerializerValidationError({"password": list(exception.messages)})

        return attrs

    def update(self, instance: User, validated_data: Any) -> User:
        """Updates user.
        First, the password is popped from updated fields,
        if in attrs it is hashed and set hashed in instance.
        Then the instance is saved (password no longer in validated data).
        """
        password = validated_data.pop("password", None)
        if password is not None:
            instance.set_password(password)
        return super().update(instance, validated_data)

    def create(self, validated_data: dict[str, Any]) -> User:
        return User.objects.create_user(**validated_data)
