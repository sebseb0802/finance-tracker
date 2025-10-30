from django.shortcuts import render, get_list_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime

from .models import User, Income, Expense, Budget


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
        # Create this income and save it to the database
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
        current_date = datetime.now()
        current_year = current_date.year
        current_month = current_date.month

        if Budget.objects.filter(category=input_category): 
            # If a budget of this category of expense exists, 
            # subtract the value of this expense from the values for remaining monthly and yearly spending of the budget
            remainingValueMonth = Budget.objects.get(category=input_category).remainingValueMonth
            remainingValueYear = Budget.objects.get(category=input_category).remainingValueYear

            Budget.objects.filter(category=input_category).update(remainingValueMonth=(remainingValueMonth-int(input_value)))

            if input_frequency == "Monthly":
                # If the frequency of the expense is monthly, then subtract 12-times the value of 
                # the expense from the remaining value to be spent of the budget for the entire year
                Budget.objects.filter(category=input_category).update(remainingValueYear=(remainingValueYear-((12-current_month+1) * int(input_value))))
            else:
                # Else, subtract only the value of the expense
                Budget.objects.filter(category=input_category).update(remainingValueYear=(remainingValueYear-int(input_value)))
        
        # Create this expense and save it to the database
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
        input_value = int(request.POST["value"]) # Convert input string to integer to avoid errors during multiplication below
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
        current_date = datetime.now()
        current_year = current_date.year
        current_month = current_date.month

        deletedBudget = False
        
        if Budget.objects.filter(category=input_category):
            # If a budget of this category already exists, delete the one that already exists, 
            # as a user cannot have more than one budget for a category
            Budget.objects.filter(category=input_category).delete()
            deletedBudget = True

        yearlyValue = 12 * input_value # yearlyValue is 12-times the monthly (input) value
        
        # Create this budget and save it to the database
        budget = Budget(user=User.objects.get(), category=input_category, value=input_value, remainingValueMonth=input_value, startDate=input_startDate, yearlyValue=yearlyValue, remainingValueYear=yearlyValue)
        budget.save()

        if Expense.objects.filter(category=input_category):
            # If expenses for this category already exist, 
            # create a list of them
            requiredExpenses = get_list_or_404(Expense.objects.filter(category=input_category))
                    
            for i in range(len(requiredExpenses)):
                # Iterate through the list of expenses and subtract their respective values from 
                # the values for remaining monthly and yearly spending of this budget
                expenseValue = requiredExpenses[i].value
                remainingValueMonth = Budget.objects.get(category=input_category).remainingValueMonth - expenseValue

                if requiredExpenses[i].frequency == "Monthly":
                    # If an expense has a monthly frequency, then subtract 12-times the value of the expense from the
                    # remaining value to be spent for the budget for this year
                    remainingValueYear = Budget.objects.get(category=input_category).remainingValueYear - ((12-current_month+1) * expenseValue)
                else:
                    # Else, subtract only the value of the expense
                    remainingValueYear = Budget.objects.get(category=input_category).remainingValueYear - expenseValue

                Budget.objects.filter(category=input_category).update(remainingValueMonth=remainingValueMonth, remainingValueYear=remainingValueYear)

        if deletedBudget == True:
            # If a previous budget was deleted, inform the user in the returned message
            return HttpResponseRedirect(f"{reverse('finance:budgets')}?message=Budget added successfully (previous budget with the same category and frequency was deleted).")
        else:
            return HttpResponseRedirect(f"{reverse('finance:budgets')}?message=Budget added successfully.")