from django.db import models
import datetime


# Create your models here.
class User(models.Model):
    username = models.CharField(default="username", max_length=200)
    password = models.CharField(default="password", max_length=200)
    is_primary_user = models.BooleanField(default=False)

    def __str__(self):
        return self.user_username
    
class FinancialObject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # A single user can have many instances of income/expenses/budgets
    value = models.IntegerField(default=0)
    startDate = models.DateField(default=datetime.date.today)
    addDate = models.DateField(default=datetime.date.today)

    class Meta:
        abstract = True # Makes the "FinancialObject" class an Abstract Base Class (ABC)

class Income(FinancialObject):
    source = models.CharField(default="N/A", max_length=200)
    frequency = models.CharField(default="Monthly", max_length=200)
    
class Expense(FinancialObject):
    source = models.CharField(default="N/A", max_length=200)
    category = models.CharField(default="Entertainment", max_length=200)
    frequency = models.CharField(default="Monthly", max_length=200)

class Budget(FinancialObject):
    yearlyValue = models.IntegerField(default=0)
    category = models.CharField(default="Entertainment", max_length=200)
    remainingValueMonth = models.IntegerField(default=0)
    remainingValueYear = models.IntegerField(default=0)

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reportType = models.CharField(default="Month", max_length=200)
    file = models.FileField(upload_to="reports/")
    creationDate = models.DateTimeField(auto_now_add=True)