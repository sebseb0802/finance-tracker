from django.urls import path

from . import views

app_name = "finance" # Sets the application namespace to "finance"
urlpatterns = [
    path("income/", views.income, name="income"),
    path("addIncome/", views.addIncome, name="addIncome"),
    path("expenses/", views.expenses, name="expenses"),
    path("addExpense", views.addExpense, name="addExpense"),
    path("budgets/", views.budgets, name="budgets"),
    path("addBudget/", views.addBudget, name="addBudget"),
    path("reports/", views.reports, name="reports"),
    path("deleteFinancialObject/", views.deleteFinancialObject, name="deleteFinancialObject"),
    path("generateReport/", views.generateReport, name="generateReport"),
    path("downloadPastReport/<int:report_id>/", views.downloadPastReport, name="downloadPastReport")
]