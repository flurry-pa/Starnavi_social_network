from rest_framework import routers
from api.viewsets import UserViewSet, PostViewSet, LikeViewSet, DislikeViewSet

router = routers.SimpleRouter()
router.register(r'user', UserViewSet)
router.register(r'post', PostViewSet)
router.register(r'like', LikeViewSet)
router.register(r'dislike', DislikeViewSet)
