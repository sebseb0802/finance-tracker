from django.shortcuts import render, get_list_or_404
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from .models import User, Income

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
        input_value = request.POST["income_value"]
        input_source = request.POST["income_source"]
        input_frequency = request.POST["income_frequency"]
        input_startDate = request.POST["income_startDate"]
    finally:
        if not input_value or not input_source or not input_frequency or not input_startDate:
            income = get_list_or_404(Income)
            return render(
                request, 
                "finance/income.html", 
                {
                    "income": income,
                    "message": "All fields must be complete."
                }
            )
        else:
            income = Income(user=User.objects.get(), income_value=input_value, income_source=input_source, income_frequency=input_frequency, income_startDate=input_startDate)
            income.save()
            return HttpResponseRedirect(f"{reverse('finance:income')}?message=Income added successfully.")