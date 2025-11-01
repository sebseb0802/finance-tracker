from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "authentication" # Sets the application namespace to "authentication"
urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("loginProcess/", views.loginProcess, name="loginProcess"),
    path("register/", views.register, name="register")
]