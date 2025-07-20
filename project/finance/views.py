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
        input_value = int(request.POST["value"])
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
        input_value = int(request.POST["value"])
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
        if Budget.objects.filter(category=input_category):
            remainingValueMonth = Budget.objects.get(category=input_category).remainingValueMonth
            remainingValueYear = Budget.objects.get(category=input_category).remainingValueYear

            Budget.objects.filter(category=input_category).update(remainingValueMonth=(remainingValueMonth-int(input_value)))
            Budget.objects.filter(category=input_category).update(remainingValueYear=(remainingValueYear-int(input_value)))
        

        expense = Expense(user=User.objects.get(), category=input_category, value=input_value, frequency=input_frequency, source=input_source, startDate=input_startDate)
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
        input_value = int(request.POST["value"])
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
        deletedBudget = False
        
        if Budget.objects.filter(category=input_category):
            Budget.objects.filter(category=input_category).delete() # User cannot have more than one budget for a category
            deletedBudget = True

        yearlyValue = 12 * input_value
        budget = Budget(user=User.objects.get(), category=input_category, value=input_value, remainingValueMonth=input_value, startDate=input_startDate, yearlyValue=yearlyValue, remainingValueYear=yearlyValue)
        budget.save()

        if Expense.objects.filter(category=input_category):
            requiredExpenses = get_list_or_404(Expense.objects.filter(category=input_category))
                    
            for i in range(len(requiredExpenses)):
                expenseValue = requiredExpenses[i].value
                remainingValueMonth = Budget.objects.filter(category=input_category).get().remainingValueMonth - expenseValue
                remainingValueYear = Budget.objects.filter(category=input_category).get().remainingValueYear - expenseValue
                Budget.objects.filter(category=input_category).update(remainingValueMonth=remainingValueMonth, remainingValueYear=remainingValueYear)

        if deletedBudget == True:
            return HttpResponseRedirect(f"{reverse('finance:budgets')}?message=Budget added successfully (previous budget with the same category and frequency was deleted).")
        else:
            return HttpResponseRedirect(f"{reverse('finance:budgets')}?message=Budget added successfully.")