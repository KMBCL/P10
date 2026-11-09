from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsAuthor(BasePermission):
    def has_object_permission(
        self,
        request: Request,
        view: APIView,
        obj: Any,
    ) -> bool:
        return obj.author == request.user


class IsProjectAuthor(BasePermission):
    def has_object_permission(
        self,
        request: Request,
        view: APIView,
        obj: Any,
    ) -> bool:
        return obj.project.author == request.user
