from django.shortcuts import render
from finance.models import User, Income, Expense
from django.db.models import Q
from datetime import datetime


# Create your views here.
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
        "dashboard/index.html", 
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