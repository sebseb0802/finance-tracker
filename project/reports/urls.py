from django.urls import path

from . import views

app_name = "reports" # Sets the application namespace to "finance"
urlpatterns = [
    path("createReport/", views.createReport, name="createReport")
]