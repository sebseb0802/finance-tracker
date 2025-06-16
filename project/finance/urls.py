from django.urls import path

from . import views

app_name = "finance" # Sets the application namespace to "finance"
urlpatterns = [
    path("", views.index, name="index"),
    path("income/", views.income, name="income"),
    path("addIncome/", views.addIncome, name="addIncome"),
    path("expenses/", views.expenses, name="expenses"),
    path("addExpense", views.addExpense, name="addExpense"),
    path("budgets/", views.budgets, name="budgets"),
    path("addBudget/", views.addBudget, name="addBudget")
]