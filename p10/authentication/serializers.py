"""Serializers and related fields for the User model."""

from typing import Any

from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    ValidationError as SerializerValidationError,
)
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as CoreValidationError


from authentication.models import User


class UserListSerializer(ModelSerializer[User]):
    """Public user representation: id and username only."""

    class Meta:
        model = User
        fields = [
            "id",
            "username",
        ]
        read_only_fields = fields


class UserRelatedField(PrimaryKeyRelatedField):
    """User relation written as a pk and read as a nested object."""

    def use_pk_only_optimization(self) -> bool:
        """Disable pk-only optimization so the full user is loaded."""
        return False

    def to_representation(self, value: User) -> dict[str, Any]:
        """Serialize the related user as a nested object."""
        return UserListSerializer(value).data


class UserSerializer(ModelSerializer[User]):
    """Full user representation with password validation and hashing."""

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
        """Build an unsaved user for UserAttributeSimilarityValidator."""
        user = User(**{key: value for key, value in attrs.items() if key != "password"})
        return user

    def validate(self, attrs: Any) -> Any:
        """Validate the password against the instance, or a temp user on create."""
        password = attrs.get("password")
        if password is not None:
            user = self.instance or self.temp_user(attrs)

            try:
                validate_password(attrs["password"], user=user)
            except CoreValidationError as exception:
                raise SerializerValidationError({"password": list(exception.messages)})

        return attrs

    def update(self, instance: User, validated_data: Any) -> User:
        """Update the user, hashing the password if provided."""
        password = validated_data.pop("password", None)
        if password is not None:
            instance.set_password(password)
        return super().update(instance, validated_data)

    def create(self, validated_data: dict[str, Any]) -> User:
        """Create the user with a hashed password."""
        return User.objects.create_user(**validated_data)
