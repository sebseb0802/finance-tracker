from django.shortcuts import render, redirect
from django.contrib.auth import authenticate 
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponseNotAllowed

from finance.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "is_primary_user"
        ]

# Create your views here.
def login(request, message=""):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("dashboard/")
        else:
            return render(
            request, 
            "registration/login.html",
            {
                'message': "Incorrect username or password."
            }
        )
    else:
        return render(
            request, 
            "registration/login.html",
            {
                'message': message
            }
        )
        
def register(request):
    users = list(User.objects.filter(is_superuser=False))
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid(): # Maybe edit to make validation rules yourself
            user = form.save(commit=False)
            if len(users) == 0:
                user.is_primary_user = True
            user.save()

            messages.success(request, "Successfully registered!")
            return redirect("authentication:login")
    else:
        form = CustomUserCreationForm()

    return render( 
        request, 
        "registration/register.html", 
        {
            'form': form,
            'users': users
        }
    )

def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return redirect("login")
    return HttpResponseNotAllowed(["POST"])