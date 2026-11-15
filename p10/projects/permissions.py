from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from projects.access import AccessManager


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


class IsProjectContributor(BasePermission):
    """Contrôle sur le projet parent de l'URL /projects/{project_pk}/...
    À placer après IsAuthenticated."""

    message = "Vous devez être contributeur du projet."

    def has_permission(self, request: Request, view: APIView) -> bool:
        return AccessManager(request.user).is_contributor(view.kwargs["project_pk"])
