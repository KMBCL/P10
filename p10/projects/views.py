"""API viewsets for projects, issues, comments and contributors."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from django.db.models.query import QuerySet
from django.db.transaction import atomic
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404

from projects.models import Comment, Contributor, Issue, Project
from projects.serializers import (
    CommentSerializer,
    IssueSerializer,
    IssueListSerializer,
    ProjectSerializer,
    ContributorSerializer,
)

from projects.permissions import (
    IsAuthor,
    IsProjectAuthor,
    IsProjectContributor,
)

if TYPE_CHECKING:
    from rest_framework.permissions import _SupportsHasPermission


class ProjectViewSet(ModelViewSet[Project]):
    """CRUD on projects the user contributes to; only the author may modify."""

    serializer_class = ProjectSerializer
    lookup_value_regex = r"\d+"

    def get_queryset(self) -> QuerySet[Project, Project]:
        """Projects the user contributes to, oldest first."""
        return (
            Project.objects.filter(contributors__user=self.request.user)
            .select_related("author")
            .order_by("created_time", "pk")
        )

    def perform_create(self, serializer: BaseSerializer[Project]) -> None:
        """Save the project and add its author as contributor, atomically."""
        with atomic():
            project = serializer.save(author=self.request.user)
            Contributor.objects.create(user=self.request.user, project=project)

    def get_permissions(self) -> Sequence[_SupportsHasPermission]:
        """Require authentication, plus authorship for writes."""
        if self.action in ("update", "partial_update", "destroy"):
            return [IsAuthenticated(), IsAuthor()]
        return [IsAuthenticated()]


class IssueViewSet(ModelViewSet[Issue]):
    """CRUD on a project's issues for its contributors; only the author may modify."""

    lookup_value_regex = r"\d+"

    def get_serializer_class(self) -> type[BaseSerializer[Issue]]:
        """Use the lightweight serializer for list, the full one otherwise."""
        if self.action == "list":
            return IssueListSerializer
        return IssueSerializer

    def get_queryset(self) -> QuerySet[Issue, Issue]:
        """Issues of the URL's project if the user contributes to it, oldest first."""
        queryset = Issue.objects.filter(
            project__id=self.kwargs["project_pk"],
            project__contributors__user=self.request.user,
        ).select_related("author", "assigned_to")
        if self.action != "list":
            queryset = queryset.select_related("project__author")
        # indexer created_time côté base
        return queryset.order_by("created_time", "pk")

    def get_permissions(self) -> Sequence[_SupportsHasPermission]:
        """Require project membership, plus authorship for writes."""
        # update is_author
        if self.action in ("update", "partial_update", "destroy"):
            return [IsAuthenticated(), IsProjectContributor(), IsAuthor()]
        return [IsAuthenticated(), IsProjectContributor()]

    def perform_create(self, serializer: BaseSerializer[Issue]) -> None:
        """Save the issue with the user as author in the URL's project."""
        serializer.save(
            author=self.request.user,
            project_id=self.kwargs["project_pk"],
        )


class CommentViewSet(ModelViewSet[Comment]):
    """CRUD on an issue's comments for project contributors; only the author may modify."""

    serializer_class = CommentSerializer

    def get_queryset(self) -> QuerySet[Comment, Comment]:
        """Comments of the URL's issue if the user contributes to its project, oldest first."""
        return (
            Comment.objects.filter(
                issue_id=self.kwargs["issue_pk"],
                issue__project_id=self.kwargs["project_pk"],
                issue__project__contributors__user=self.request.user,
            )
            .select_related("author")
            .order_by("created_time", "pk")
        )

    def get_permissions(self) -> Sequence[_SupportsHasPermission]:
        """Require project membership, plus authorship for writes."""
        if self.action in ("update", "partial_update", "destroy"):
            return [IsAuthenticated(), IsProjectContributor(), IsAuthor()]
        return [IsAuthenticated(), IsProjectContributor()]

    def perform_create(self, serializer: BaseSerializer[Comment]) -> None:
        """Save the comment on the URL's issue, 404 if not in the URL's project."""
        issue = get_object_or_404(
            Issue,
            pk=self.kwargs["issue_pk"],
            project_id=self.kwargs["project_pk"],
        )
        serializer.save(author=self.request.user, issue=issue)


class ContributorViewSet(ModelViewSet[Contributor]):
    """Lists, adds and removes project contributors; writes reserved to the project author."""

    serializer_class = ContributorSerializer
    http_method_names = ["get", "post", "delete", "head", "options"]

    def get_queryset(self) -> QuerySet[Contributor, Contributor]:
        """Contributors of the URL's project if the user contributes to it, oldest first."""
        return (
            Contributor.objects.filter(
                project_id=self.kwargs["project_pk"],
                project__contributors__user=self.request.user,
            )
            .select_related("user")
            .order_by("created_time", "pk")
        )

    def get_permissions(self) -> Sequence[_SupportsHasPermission]:
        """Require project membership, plus project authorship for writes."""
        if self.action in ("create", "destroy"):
            return [
                IsAuthenticated(),
                IsProjectContributor(),
                IsProjectAuthor(),
            ]
        return [IsAuthenticated(), IsProjectContributor()]

    def perform_create(self, serializer: BaseSerializer[Contributor]) -> None:
        """Save the contributor in the URL's project."""
        serializer.save(project_id=self.kwargs["project_pk"])

    def perform_destroy(self, instance: Contributor) -> None:
        """Remove the contributor, unless it is the project author."""
        if instance.user_id == instance.project.author_id:
            raise PermissionDenied("L'auteur du projet ne peut pas être retiré.")
        super().perform_destroy(instance)
