from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from projects.access import AccessManager


class IsAuthor(BasePermission):
    """Allows access only to the author of the object."""

    def has_object_permission(
        self,
        request: Request,
        view: APIView,
        obj: Any,
    ) -> bool:
        """Return True if the user is the object's author."""
        return obj.author == request.user


class IsProjectAuthor(BasePermission):
    """Allows access only to the author of the URL's project; place after IsProjectContributor."""

    message = "Vous devez être l'auteur du projet."

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Return True if the user authored the URL's project."""
        return AccessManager(request.user).is_project_author(
            view.kwargs["project_pk"]
        )


class IsProjectContributor(BasePermission):
    """Allows access only to contributors of the URL's project; place after IsAuthenticated."""

    message = "Vous devez être contributeur du projet."

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Return True if the user contributes to the URL's project."""
        return AccessManager(request.user).is_contributor(view.kwargs["project_pk"])
