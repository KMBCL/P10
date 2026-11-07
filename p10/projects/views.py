from django.db.models.query import QuerySet
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet

from projects.models import Comment, Contributor, Issue, Project
from projects.serializers import CommentSerializer, IssueSerializer, ProjectSerializer


class ProjectViewSet(ModelViewSet[Project]):

    serializer_class = ProjectSerializer

    def get_queryset(self) -> QuerySet[Project, Project]:
        return Project.objects.all()

    def perform_create(self, serializer: BaseSerializer[Project]) -> None:
        # Le créateur devient l'auteur ET le premier contributeur du projet.
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)


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
