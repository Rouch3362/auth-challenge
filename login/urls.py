from django.urls import path

from . import views

urlpatterns = [
    path("", views.loginUser , name="login-user")
]