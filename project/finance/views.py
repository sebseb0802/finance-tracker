from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime

from django.db.models import Q
from django.template.loader import render_to_string
from weasyprint import HTML
from io import BytesIO
from django.http import FileResponse
from django.core.files.base import ContentFile

from .models import User, Income, Expense, Budget, Report


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
        
def reports(request):
    message = request.GET.get("message", "")
    reports = Report.objects.all()
    return render(
        request, 
        "finance/reports.html", 
        {
            "reports": reports,
            "message": message
        }
    )

def generateReport(request):
    def sumFinancialObjectsFromList(l, timeframe="Month"):
        sum = 0
        for i in range(len(l)):
            if l[i].frequency == "Monthly" and timeframe == "Year":
                # If the FinancialObject has a monthly frequency, and the specified timeframe for the summation is a year,
                # then multiply the value of the FinancialObject by 12 to account for this
                value_to_add = (12-l[i].startDate.month+1) * l[i].value
            else:
                # Else, simply add the value of the FinancialObject
                value_to_add = l[i].value
            
            sum += value_to_add

        return sum

    user = User.objects.get()

    input_type = request.POST["type"]

    budgets = Budget.objects.all()

    current_datetime = datetime.now()

    if input_type == "Month":
        current_month = current_datetime.month

        # Change current_month to its equivalent English-language string for use in displaying in the file
        if current_month == 1:
            current_month_name = "January"
        elif current_month == 2:
            current_month_name = "February"
        elif current_month == 3:
            current_month_name = "March"
        elif current_month == 4:
            current_month_name = "April"
        elif current_month == 5:
            current_month_name = "May"
        elif current_month == 6:
            current_month_name = "June"
        elif current_month == 7:
            current_month_name = "July"
        elif current_month == 8:
            current_month_name = "August"
        elif current_month == 9:
            current_month_name = "September"
        elif current_month == 10:
            current_month_name = "October"
        elif current_month == 11:
            current_month_name = "November"
        else:
            current_month_name = "December"      
        
        # Create lists of relevant Income objects for the current month by filtering with Q()
        current_month_income = list(Income.objects.filter(Q(frequency="Monthly") | (Q(frequency="One-off") & Q(startDate__month=str(current_month)))))

        # Create lists of relevant Expense objects for the current month by filtering with Q()
        current_month_expenses = list(Expense.objects.filter(Q(frequency="Monthly") | (Q(frequency="One-off") & Q(startDate__month=str(current_month)))))

        # Sum all income for the current month
        current_month_income_total = sumFinancialObjectsFromList(current_month_income)

        # Sum all expenses for the current month
        current_month_expenses_total = sumFinancialObjectsFromList(current_month_expenses)

        # Calculate net income for the current month
        current_month_net_income = current_month_income_total - current_month_expenses_total

        report_text = render_to_string('finance/monthly-report-template.html', {
            'user': user,
            'current_month_name': current_month_name,
            'current_month_income_total': current_month_income_total,
            'current_month_expenses_total': current_month_expenses_total,
            'current_month_net_income': current_month_net_income,
            'income': current_month_income,
            'expenses': current_month_expenses,
            'budgets': budgets
        })
        pdf_bytes = HTML(string=report_text).write_pdf()
        reportType = "Month"
    else:
        current_year = current_datetime.year
        
        # Create lists of relevant Income objects for the current year by filtering with Q()
        current_year_income = list(Income.objects.filter(Q(frequency="Monthly") | (Q(frequency="One-off") & Q(startDate__year=str(current_year))) | Q(frequency="Yearly")))

        # Create lists of relevant Expense objects for the current year by filtering with Q()
        current_year_expenses = list(Expense.objects.filter(Q(frequency="Monthly") | (Q(frequency="One-off") & Q(startDate__year=str(current_year))) | Q(frequency="Yearly")))

        # Sum all income for the current year
        current_year_income_total = sumFinancialObjectsFromList(current_year_income, "Year")

        # Sum all expenses for the current year
        current_year_expenses_total = sumFinancialObjectsFromList(current_year_expenses, "Year")

        # Calculate net income for the current year
        current_year_net_income = current_year_income_total - current_year_expenses_total

        report_text = render_to_string('finance/yearly-report-template.html', {
            'user': user,
            'current_year': current_year,
            'current_year_income_total': current_year_income_total,
            'current_year_expenses_total': current_year_expenses_total,
            'current_year_net_income': current_year_net_income,
            'income': current_year_income,
            'expenses': current_year_expenses,
            'budgets': budgets
        })

        pdf_bytes = HTML(string=report_text).write_pdf()
        reportType = "Year"

    report = Report(user=user, reportType=reportType)
    report.file.save(f'{current_datetime}_report.pdf', ContentFile(pdf_bytes))
    report.save()

    return FileResponse(BytesIO(pdf_bytes), filename=f'{current_datetime}_{reportType}_report.pdf', as_attachment=True)

def downloadPastReport(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    return FileResponse(report.file, as_attachment=True, filename=f'{report.creationDate}_{report.reportType}_report.pdf')