from django.urls import path

from . import views

urlpatterns = [
    path("verify/", views.verifyNumber , name="verify-user-number"),
    path("", views.loginUser , name="login-user")
]