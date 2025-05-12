from django.urls import path

from . import views

app_name = "finance" # Sets the application namespace to "finance"
urlpatterns = [
    path("", views.index, name="index"),
    path("income/", views.income, name="income"),
    path("addIncome/", views.addIncome, name="addIncome")
]