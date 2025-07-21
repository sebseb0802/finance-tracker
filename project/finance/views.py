from django.shortcuts import render, get_list_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q

from .models import User, Income, Expense, Budget

from datetime import datetime


def index(request):
    # Avoid repetition of summation of FinancialObjects below (4 times) through the use of the following function
    def sumFinancialObjectsFromList(l, timeframe="Month"):
        sum = 0
        for i in range(len(l)):
            if l[i].frequency == "Monthly" and timeframe == "Year":
                # If the FinancialObject has a monthly frequency, and the specified timeframe for the summation is a year,
                # then multiply the value of the FinancialObject by 12 to account for this
                value_to_add = 12 * l[i].value
            else:
                # Else, simply add the value of the FinancialObject
                value_to_add = l[i].value
            
            sum += value_to_add

        return sum
    
    user = User.objects.get()

    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month
    
    # Create lists of relevant Income objects for the current month/year by filtering with Q()
    current_month_income = list(Income.objects.filter(Q(frequency="Monthly") | (Q(frequency="One-off") & Q(startDate__month=str(current_month))) | Q(startDate__month=str(current_month))))
    current_year_income = list(Income.objects.filter(Q(frequency="Monthly") | (Q(frequency="One-off") & Q(startDate__year=str(current_year))) | Q(frequency="Yearly")))

    # Create lists of relevant Expense objects for the current month/year by filtering with Q()
    current_month_expenses = list(Expense.objects.filter(Q(frequency="Monthly") | (Q(frequency="One-off") & Q(startDate__month=str(current_month))) | Q(startDate__month=str(current_month))))
    current_year_expenses = list(Expense.objects.filter(Q(frequency="Monthly") | (Q(frequency="One-off") & Q(startDate__year=str(current_year))) | Q(frequency="Yearly")))


    # Sum all income for the current month/year
    current_month_income_total = sumFinancialObjectsFromList(current_month_income)
    current_year_income_total = sumFinancialObjectsFromList(current_year_income, "Year")

    # Sum all expenses for the current month/year
    current_month_expenses_total = sumFinancialObjectsFromList(current_month_expenses)
    current_year_expenses_total = sumFinancialObjectsFromList(current_year_expenses, "Year")

    # Calculate net income for both the current month and the current year
    current_month_net_income = current_month_income_total - current_month_expenses_total
    current_year_net_income = current_year_income_total - current_year_expenses_total

    # Change current_month to its equivalent English-language string for use in displaying in index.html
    if current_month == 1:
        current_month = "January"
    elif current_month == 2:
        current_month = "February"
    elif current_month == 3:
        current_month = "March"
    elif current_month == 4:
        current_month = "April"
    elif current_month == 5:
        current_month = "May"
    elif current_month == 6:
        current_month = "June"
    elif current_month == 7:
        current_month = "July"
    elif current_month == 8:
        current_month = "August"
    elif current_month == 9:
        current_month = "September"
    elif current_month == 10:
        current_month = "October"
    elif current_month == 11:
        current_month = "November"
    else:
        current_month = "December"

    return render(
        request, 
        "finance/index.html", 
        {
            "user": user,
            "current_month": current_month,
            "current_year": current_year,
            "current_month_income_total": current_month_income_total,
            "current_year_income_total": current_year_income_total,
            "current_month_expenses_total": current_month_expenses_total,
            "current_year_expenses_total": current_year_expenses_total,
            "current_month_net_income": current_month_net_income,
            "current_year_net_income": current_year_net_income
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
        if Budget.objects.filter(category=input_category): 
            # If a budget of this category of expense exists, 
            # subtract the value of this expense from the values for remaining monthly and yearly spending of the budget
            remainingValueMonth = Budget.objects.get(category=input_category).remainingValueMonth
            remainingValueYear = Budget.objects.get(category=input_category).remainingValueYear

            Budget.objects.filter(category=input_category).update(remainingValueMonth=(remainingValueMonth-int(input_value)))

            if input_frequency == "Monthly":
                # If the frequency of the expense is monthly, then subtract 12-times the value of 
                # the expense from the remaining value to be spent of the budget for the entire year
                Budget.objects.filter(category=input_category).update(remainingValueYear=(remainingValueYear-(12 * int(input_value))))
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
                remainingValueMonth = Budget.objects.filter(category=input_category).get().remainingValueMonth - expenseValue

                if requiredExpenses[i].frequency == "Monthly":
                    # If an expense has a monthly frequency, then subtract 12-times the value of the expense from the
                    # remaining value to be spent for the budget for this year
                    remainingValueYear = Budget.objects.filter(category=input_category).get().remainingValueYear - (12 * expenseValue)
                else:
                    # Else, subtract only the value of the expense
                    remainingValueYear = Budget.objects.filter(category=input_category).get().remainingValueYear - expenseValue

                Budget.objects.filter(category=input_category).update(remainingValueMonth=remainingValueMonth, remainingValueYear=remainingValueYear)

        if deletedBudget == True:
            # If a previous budget was deleted, inform the user in the returned message
            return HttpResponseRedirect(f"{reverse('finance:budgets')}?message=Budget added successfully (previous budget with the same category and frequency was deleted).")
        else:
            return HttpResponseRedirect(f"{reverse('finance:budgets')}?message=Budget added successfully.")