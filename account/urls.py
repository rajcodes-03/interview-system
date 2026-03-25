from django.urls import path
from . import views

urlpatterns = [
    path("", views.account, name="login"),
    path("login/", views.account, name="login"),  
    path("register/", views.register, name="register"),
] 