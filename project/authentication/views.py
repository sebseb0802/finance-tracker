from django.shortcuts import render, redirect
from django.contrib.auth import authenticate

# Create your views here.
def login(request, message=""):
    return render(
        request, 
        "registration/login.html",
        {
            'message': message
        }
    )

def loginProcess(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            return redirect("dashboard/")
        else:
            return login(
                request,
                "Incorrect username or password."
            )
        
def register(request):
    return render(
        request,
        "registration/register.html"
    )

def logout(request):
    request.user.is_authenticated = False
    return render(
        request, 
        "registration/login.html"
    )