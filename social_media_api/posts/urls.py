from rest_framework import routers
from .views import PostViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r"posts", PostViewSet, basename="posts")
router.register(r"comments", CommentViewSet, basename="comments")

urlpatterns = router.urls
