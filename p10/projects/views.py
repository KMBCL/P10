from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from django.db.models.query import QuerySet
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from projects.models import Comment, Contributor, Issue, Project
from projects.serializers import CommentSerializer, IssueSerializer, ProjectSerializer

from projects.permissions import IsAuthor

if TYPE_CHECKING:
    from rest_framework.permissions import _SupportsHasPermission


class ProjectViewSet(ModelViewSet[Project]):

    serializer_class = ProjectSerializer

    def get_queryset(self) -> QuerySet[Project, Project]:
        return Project.objects.all()

    def perform_create(self, serializer: BaseSerializer[Project]) -> None:
        # Le créateur devient l'auteur ET le premier contributeur du projet.
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)

    def get_permissions(self) -> Sequence[_SupportsHasPermission]:
        if self.action in ("update", "partial_update", "destroy"):
            return [IsAuthenticated(), IsAuthor()]
        return [IsAuthenticated()]


class IssueViewSet(ModelViewSet[Issue]):

    serializer_class = IssueSerializer

    def get_queryset(self) -> QuerySet[Issue, Issue]:
        return Issue.objects.all()

    def perform_create(self, serializer: BaseSerializer[Issue]) -> None:
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet[Comment]):

    serializer_class = CommentSerializer

    def get_queryset(self) -> QuerySet[Comment, Comment]:
        return Comment.objects.all()

    def perform_create(self, serializer: BaseSerializer[Comment]) -> None:
        serializer.save(author=self.request.user)
