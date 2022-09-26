from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)


# /users
urlpatterns = [
    path('/login', TokenObtainPairView.as_view(), name='login')
]