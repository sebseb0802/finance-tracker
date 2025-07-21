from django.urls import path

from . import views

app_name = "authentication" # Sets the application namespace to "finance"
urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout")
]