from django.db import models
import datetime


# Create your models here.
class User(models.Model):
    user_username = models.CharField(max_length=200)

    def __str__(self):
        return self.user_username

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # A single user can have many instances of income
    income_value = models.IntegerField(default=0)
    income_source = models.CharField(default="Work", max_length=200)
    income_frequency = models.CharField(default="Monthly", max_length=200)
    income_startDate = models.DateField(default=datetime.date.today)

    def __str__(self):
        return str(self.income_value)