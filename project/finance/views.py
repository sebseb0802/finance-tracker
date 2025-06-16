from django.shortcuts import render, get_list_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import User, Income, Expense, Budget

# Create your views here.
def index(request):
    user = User.objects.get()
    return render(
        request, 
        "finance/index.html", 
        {
            "user": user
        }
    )

def income(request):
    message = request.GET.get("message", "")
    income = Income.objects.all()
    return render(
        request, 
        "finance/income.html", 
        {
            "income": income,
            "message": message
        }
    )

def addIncome(request):
    try:
        input_value = request.POST["value"]
        input_source = request.POST["source"]
        input_frequency = request.POST["frequency"]
        input_startDate = request.POST["startDate"]
    except:
        income = Income.objects.all()
        return render(
            request, 
            "finance/income.html", 
            {
                "income": income,
                "message": "All fields must be complete."
            }
        )
    else:
        income = Income(user=User.objects.get(), value=input_value, source=input_source, frequency=input_frequency, startDate=input_startDate)
        income.save()
        return HttpResponseRedirect(f"{reverse('finance:income')}?message=Income added successfully.")
        
def expenses(request):
    message = request.GET.get("message", "")
    expenses = Expense.objects.all()
    return render(
        request, 
        "finance/expenses.html", 
        {
            "expenses": expenses,
            "message": message
        }
    )

def addExpense(request):
    try:
        input_category = request.POST["category"]
        input_value = request.POST["value"]
        input_source = request.POST["source"]
        input_frequency = request.POST["frequency"]
        input_startDate = request.POST["startDate"]
    except:
        expenses = Expense.objects.all()
        return render(
            request, 
            "finance/expenses.html", 
            {
                "expenses": expenses,
                "message": "All fields must be complete."
            }
        )
    else:
        expense = Expense(user=User.objects.get(), category=input_category, value=input_value, source=input_source, frequency=input_frequency, startDate=input_startDate)
        expense.save()
        return HttpResponseRedirect(f"{reverse('finance:expenses')}?message=Expense added successfully.")
    
def budgets(request):
    message = request.GET.get("message", "")
    budgets = Budget.objects.all()
    return render(
        request, 
        "finance/budgets.html", 
        {
            "budgets": budgets,
            "message": message
        }
    )

def addBudget(request):
    try:
        input_category = request.POST["category"]
        input_value = request.POST["value"]
        input_frequency = request.POST["frequency"]
        input_startDate = request.POST["startDate"]
    except:
        budgets = Budget.objects.all()
        return render(
            request, 
            "finance/budgets.html", 
            {
                "budgets": budgets,
                "message": "All fields must be complete."
            }
        )
    else:
        budget = Budget(user=User.objects.get(), category=input_category, value=input_value, remainingValue = input_value, frequency=input_frequency, startDate=input_startDate)
        budget.save()
        return HttpResponseRedirect(f"{reverse('finance:budgets')}?message=Budget added successfully.")