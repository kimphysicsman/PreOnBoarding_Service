from base64 import urlsafe_b64decode
from django.urls import path

from post.views import (
    PostView,
    RecoverPostView,
)

# /posts
urlpatterns = [
    path('', PostView.as_view()),
    path('/<int:post_id>', PostView.as_view()),
    path('/<int:post_id>/recover', RecoverPostView.as_view()),
]
