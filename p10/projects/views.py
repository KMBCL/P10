from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from django.db.models.query import QuerySet
from django.db.transaction import atomic
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from projects.models import Comment, Contributor, Issue, Project
from projects.serializers import (
    CommentSerializer,
    IssueSerializer,
    ProjectSerializer,
    ContributorSerializer,
)

from projects.permissions import IsAuthor, IsProjectAuthor

if TYPE_CHECKING:
    from rest_framework.permissions import _SupportsHasPermission


class ProjectViewSet(ModelViewSet[Project]):

    serializer_class = ProjectSerializer
    # Reprise par les routes imbriquées pour project_pk : un id non numérique
    # donne une 404 à la résolution d'URL au lieu d'une 500 en SQL.
    lookup_value_regex = r"\d+"

    def get_queryset(self) -> QuerySet[Project, Project]:
        return Project.objects.filter(contributors__user=self.request.user)

    def perform_create(self, serializer: BaseSerializer[Project]) -> None:
        # Le créateur devient l'auteur ET le premier contributeur du projet.
        with atomic():
            project = serializer.save(author=self.request.user)
            Contributor.objects.create(user=self.request.user, project=project)

    def get_permissions(self) -> Sequence[_SupportsHasPermission]:
        if self.action in ("update", "partial_update", "destroy"):
            return [IsAuthenticated(), IsAuthor()]
        return [IsAuthenticated()]


class IssueViewSet(ModelViewSet[Issue]):

    serializer_class = IssueSerializer

    def get_queryset(self) -> QuerySet[Issue, Issue]:
        return Issue.objects.filter(project__contributors__user=self.request.user)

    def get_permissions(self) -> Sequence[_SupportsHasPermission]:
        if self.action in ("update", "partial_update", "destroy"):
            return [IsAuthenticated(), IsAuthor()]
        return [IsAuthenticated()]

    def perform_create(self, serializer: BaseSerializer[Issue]) -> None:
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet[Comment]):

    serializer_class = CommentSerializer

    def get_queryset(self) -> QuerySet[Comment, Comment]:
        return Comment.objects.filter(
            issue__project__contributors__user=self.request.user
        )

    def get_permissions(self) -> Sequence[_SupportsHasPermission]:
        if self.action in ("update", "partial_update", "destroy"):
            return [IsAuthenticated(), IsAuthor()]
        return [IsAuthenticated()]

    def perform_create(self, serializer: BaseSerializer[Comment]) -> None:
        serializer.save(author=self.request.user)


class ContributorViewSet(ModelViewSet[Contributor]):

    serializer_class = ContributorSerializer

    def get_queryset(self) -> QuerySet[Contributor, Contributor]:
        return Contributor.objects.filter(project__contributors__user=self.request.user)

    def get_permissions(self) -> Sequence[_SupportsHasPermission]:
        if self.action in ("update", "partial_update", "destroy"):
            return [IsAuthenticated(), IsProjectAuthor()]
        return [IsAuthenticated()]

    def perform_destroy(self, instance: Contributor) -> None:
        if instance.user_id == instance.project.author_id:
            raise PermissionDenied("L'auteur du projet ne peut pas être retiré.")
        super().perform_destroy(instance)
