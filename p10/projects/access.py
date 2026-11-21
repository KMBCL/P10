from __future__ import annotations

from typing import TYPE_CHECKING

from projects.models import Contributor, Project

if TYPE_CHECKING:
    from authentication.models import User


class AccessManager:
    """Access rules: who is allowed to do what on a project."""

    def __init__(self, user: User) -> None:
        self.user = user

    def is_contributor(self, project_id: int | str) -> bool:
        return Contributor.objects.filter(
            project_id=project_id, user=self.user
        ).exists()

    def is_project_author(self, project_id: int | str) -> bool:
        return Project.objects.filter(pk=project_id, author=self.user).exists()
