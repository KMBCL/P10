"""Nested URL routes for projects, contributors, issues and comments."""

from rest_framework_nested import routers

from projects.views import (
    CommentViewSet,
    ContributorViewSet,
    IssueViewSet,
    ProjectViewSet,
)

router = routers.SimpleRouter()
router.register("projects", ProjectViewSet, basename="project")
projects_router = routers.NestedSimpleRouter(
    router,
    "projects",
    lookup="project",
)

projects_router.register(
    "contributors",
    ContributorViewSet,
    basename="project-contributor",
)

projects_router.register(
    "issues",
    IssueViewSet,
    basename="project-issue",
)

issues_routeur = routers.NestedSimpleRouter(
    projects_router,
    "issues",
    lookup="issue",
)

issues_routeur.register(
    "comments",
    CommentViewSet,
    basename="issue-comment",
)

urlpatterns = router.urls + projects_router.urls + issues_routeur.urls
