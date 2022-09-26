from base64 import urlsafe_b64decode
from django.urls import path

from post.views import PostView

urlpatterns = [
    path('', PostView.as_view())
]
