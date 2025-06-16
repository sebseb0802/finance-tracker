from django.db import models
import datetime


# Create your models here.
class User(models.Model):
    user_username = models.CharField(max_length=200)

    def __str__(self):
        return self.user_username
    
class FinancialObject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # A single user can have many instances of income
    source = models.CharField(default="N/A", max_length=200)
    value = models.IntegerField(default=0)
    frequency = models.CharField(default="Monthly", max_length=200)
    startDate = models.DateField(default=datetime.date.today)
    addDate = models.DateField(default=datetime.date.today)

    class Meta:
        abstract = True # Makes the "FinancialObject" class an Abstract Base Class (ABC)

class Income(FinancialObject):
    pass
    
class Expense(FinancialObject):
    category = models.CharField(default="Entertainment", max_length=200)