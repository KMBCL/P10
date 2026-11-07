from rest_framework.routers import SimpleRouter

from projects.views import CommentViewSet, IssueViewSet, ProjectViewSet

router = SimpleRouter()
router.register("projects", ProjectViewSet, basename="project")
router.register("issues", IssueViewSet, basename="issue")
router.register("comments", CommentViewSet, basename="comment")

urlpatterns = router.urls
