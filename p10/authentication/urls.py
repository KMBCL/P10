from rest_framework.routers import SimpleRouter

from authentication.view import UserViewset

router = SimpleRouter()
router.register("user", UserViewset, basename="user")

urlpatterns = router.urls
