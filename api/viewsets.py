from rest_framework.viewsets import ModelViewSet
from api.serializers import UserSerializer, PostSerializer, LikeSerializer, DislikeSerializer
from sn.models import User, Post, Like, Dislike


class UserViewSet(ModelViewSet):
    """ API endpoint that allows users to be viewed or edited """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class LikeViewSet(ModelViewSet):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()


class DislikeViewSet(ModelViewSet):
    serializer_class = DislikeSerializer
    queryset = Dislike.objects.all()
