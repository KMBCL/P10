from __future__ import annotations

from typing import TYPE_CHECKING

from projects.models import Contributor

if TYPE_CHECKING:
    from authentication.models import User


class AccessManager:
    """Règles d'accès : qui a le droit de faire quoi sur un projet."""

    def __init__(self, user: User) -> None:
        self.user = user

    def is_contributor(self, project_id: int | str) -> bool:
        return Contributor.objects.filter(
            project_id=project_id, user=self.user
        ).exists()
