from django.urls import path
from .views import account, register

urlpatterns = [
    path("", account, name="login"),
    path("login/", account, name="login"),  
    path("register/", register, name="register"),
]