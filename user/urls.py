from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from user.views import UserView

# /users
urlpatterns = [
    path('/login', TokenObtainPairView.as_view(), name='login'),
    path('', UserView.as_view(), name='user_view')
]