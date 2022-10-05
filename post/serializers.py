from rest_framework import serializers

from post.models import (
    Post as PostModel,
    Like as LikeModel,
    Hashtag as HashtagModel,
)

class PostModelSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    hashtags = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()


    def get_user(self, obj):
        return obj.user.username
    
    def get_hashtags(self, obj):
        hashtag_objs = obj.hashtag_set.all()
        hashtag_words = [obj.name for obj in hashtag_objs]

        return hashtag_words

    def get_like_count(self, obj):
        return obj.like_set.all().count()

    def get_is_liked(self, obj):
        viewer = self.context.get('viewer', None)

        if not viewer or not viewer.is_authenticated:
            return False

        if obj.like_set.filter(user=viewer).count() == 0:
            return False
        return True
        
    
    class Meta:
        model = PostModel
        fields = ["id", "title", "content", "user", "views", "is_active", "created_date",
                  "hashtags", "like_count", "is_liked"]


class PostModelListSerializer(PostModelSerializer):
    class Meta:
        model = PostModel
        fields = ["id", "title", "content", "user", "views", "is_active", "created_date",
                  "hashtags", "like_count"]