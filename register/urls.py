from django.urls import path

from . import views

urlpatterns = [
    path("" , views.register, name="register-user"),
    path("update-info/", views.updateInfo , name="update-user")
]