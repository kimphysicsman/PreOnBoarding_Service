from django.contrib import admin

from post.models import (
    Post as PostModel,
    Like as LikeModel,
    Hashtag as HashtagModel,
    PostHashtag as PostHashtagModel
)

admin.site.register(PostModel)
admin.site.register(LikeModel)
admin.site.register(HashtagModel)
admin.site.register(PostHashtagModel)