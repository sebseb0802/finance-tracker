from django.urls import path

from . import views

app_name = "dashboard" # Sets the application namespace to "finance"
urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard")
]