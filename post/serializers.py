from rest_framework import serializers

from post.models import (
    Post as PostModel,
    Like as LikeModel,
    Hashtag as HashtagModel,
)

class PostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = "__all__"