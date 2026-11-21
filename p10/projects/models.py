"""Models for projects, issues, comments and contributors."""

from __future__ import annotations

from typing import TYPE_CHECKING

from datetime import datetime
from uuid import uuid4, UUID
from django.conf import settings
from django.db import models

if TYPE_CHECKING:
    from authentication.models import User


class Project(models.Model):
    """Software project owned by an author and shared with contributors."""

    class TypeTag(models.TextChoices):
        """Target platform of the project."""

        BACK_END = "BACK_END", "Back-end"
        FRONT_END = "FRONT_END", "Front-end"
        IOS = ("IOS", "iOS")
        ANDROID = "ANDROID", "Android"

    author: models.ForeignKey[User, User] = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
    )
    name: models.CharField[str, str] = models.CharField(max_length=150)
    description: models.TextField[str, str] = models.TextField()
    project_type: models.CharField[str, str] = models.CharField(
        choices=TypeTag.choices,
        max_length=20,
        default=TypeTag.BACK_END,
    )
    created_time: models.DateTimeField[datetime, datetime] = models.DateTimeField(
        auto_now_add=True
    )


class Issue(models.Model):
    """Task, bug or feature tracked within a project."""

    class TypeTag(models.TextChoices):
        """Nature of the issue."""

        BUG = "BUG", "Bug"
        TASK = "TASK", "Tâche"
        FEATURE = "FEATURE", "Fonctionnalité"

    class PriorityTag(models.TextChoices):
        """Priority level of the issue."""

        HIGH = "HIGH", "Haute"
        MEDIUM = "MEDIUM", "Moyenne"
        LOW = "LOW", "Faible"

    class StatusTag(models.TextChoices):
        """Progress status of the issue."""

        TO_DO = "TO_DO", "A faire"
        FINISHED = "FINISHED", "Terminée"
        IN_PROGRESS = "IN_PROGRESS", "EN cours"

    author: models.ForeignKey[User, User] = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="issues",
    )
    project: models.ForeignKey[Project, Project] = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, related_name="issues"
    )
    name: models.CharField[str, str] = models.CharField(max_length=150)
    description: models.TextField[str, str] = models.TextField()
    status: models.CharField[str, str] = models.CharField(
        choices=StatusTag.choices,
        max_length=20,
        default=StatusTag.TO_DO,
    )
    priority: models.CharField[str, str] = models.CharField(
        choices=PriorityTag.choices,
        max_length=20,
        default=PriorityTag.LOW,
    )
    assigned_to: models.ForeignKey[User, User] = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="assigned_issues",
        null=True,
        blank=True,
    )
    issue_type: models.CharField[str, str] = models.CharField(
        choices=TypeTag.choices,
        max_length=20,
        default=TypeTag.BUG,
    )
    created_time: models.DateTimeField[datetime, datetime] = models.DateTimeField(
        auto_now_add=True
    )


class Comment(models.Model):
    """Comment posted on an issue, identified by a UUID."""

    id: models.UUIDField[UUID, UUID] = models.UUIDField(
        primary_key=True, default=uuid4, editable=False
    )
    author: models.ForeignKey[User, User] = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    issue: models.ForeignKey[Issue, Issue] = models.ForeignKey(
        to=Issue, on_delete=models.CASCADE, related_name="comments"
    )
    description: models.TextField[str, str] = models.TextField()
    created_time: models.DateTimeField[datetime, datetime] = models.DateTimeField(
        auto_now_add=True
    )


class Contributor(models.Model):
    """Membership link granting a user access to a project."""

    user: models.ForeignKey[User, User] = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contributions",
    )
    project: models.ForeignKey[Project, Project] = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name="contributors",
    )
    created_time: models.DateTimeField[datetime, datetime] = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("user", "project")
