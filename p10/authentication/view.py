from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from django.db.models.query import QuerySet
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny

from authentication.models import User
from authentication.serializers import UserSerializer, UserListSerializer

if TYPE_CHECKING:
    from rest_framework.permissions import _SupportsHasPermission


class UserViewset(ModelViewSet[User]):

    def get_serializer_class(self) -> type[BaseSerializer[User]]:
        if self.action == "list":
            return UserListSerializer
        return UserSerializer

    def get_permissions(self) -> Sequence[_SupportsHasPermission]:
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self) -> QuerySet[User, User]:
        queryset = User.objects.filter(is_active=True).order_by("pk")
        if self.action != "list":
            return queryset.filter(pk=self.request.user.pk)

        username = self.request.GET.get("username")
        if username is None:
            return queryset.none()

        return queryset.filter(username=username)
