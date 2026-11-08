from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from django.db.models.query import QuerySet
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response

from authentication.models import User
from authentication.serializers import UserSerializer

if TYPE_CHECKING:
    from rest_framework.permissions import _SupportsHasPermission


class UserViewset(ModelViewSet[User]):

    serializer_class = UserSerializer

    # def get_queryset(self) -> QuerySet[User, User]:
    #     return User.objects.all()

    def get_permissions(self) -> Sequence[_SupportsHasPermission]:
        if self.action == "create":
            return [AllowAny()]
        return super().get_permissions()

    def get_queryset(self) -> QuerySet[User, User]:
        queryset = User.objects.filter(is_active=True)
        username = self.request.GET.get("username")
        if username is not None:
            queryset = queryset.filter(username=username)

        return queryset
