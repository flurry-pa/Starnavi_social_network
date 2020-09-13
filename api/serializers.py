from rest_framework import serializers
from sn.models import User, Post, Like, Dislike


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'is_superuser']
        """
        possible default fields
         {
            "id": 1,
            "password": "pbkdf2_sha256$216000$GVsJru1GZVNM$uLBig/dV2ANMzhTe0Y3AHP22cWiQwaRieBtVVclsX94=",
            "last_login": "2020-09-05T20:09:10.353238Z",
            "is_superuser": true,
            "username": "admin",
            "first_name": "",
            "last_name": "",
            "email": "admin@gmail.com",
            "is_staff": true,
            "is_active": true,
            "date_joined": "2020-09-04T23:55:32.333182Z",
            "groups": [],
            "user_permissions": []
        },
        """


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        """
        {
            "id": 1,
            "title": "post_u1_1_title",
            "content": "post_u1_1_content",
            "pub_date": "2020-09-06T20:11:44.573168Z",
            "author": 2
        },
        """


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'
        """
        {
            "id": 1,
            "title": "like_u1_p8_title",
            "date": "2020-09-12T15:37:21.761434Z",
            "user": 1,
            "post": 8
        },
        """


class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        fields = '__all__'
        """
        {
            "id": 4,
            "title": "dislike_u9_p8_title",
            "date": "2020-09-13T13:54:52.335630Z",
            "user": 9,
            "post": 8
        }
        """
