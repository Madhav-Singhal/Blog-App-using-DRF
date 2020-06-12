from django.conf.urls import url
from django.contrib import admin

from .views import (
    UserCreateAPIView,
    UserLoginAPIView
    )

urlpatterns = [
    url('login/', UserLoginAPIView.as_view(), name='login'),
    url('register/', UserCreateAPIView.as_view(), name='register'),
]