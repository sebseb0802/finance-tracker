from django.shortcuts import redirect, render
from django.contrib.auth import authenticate 
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponseNotAllowed

from finance.models import User, SecondaryUserCode

import uuid

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
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            # If the user credentials are valid, 
            # then create a session and log the user in
            auth_login(request, user)

            return redirect("dashboard:dashboard")
        else:
            # If the user credentials are invalid,
            # then redirect the user to the log in page
            return redirect("authentication:login")
    else:
        return render(
            request, 
            "registration/login.html"
        )
        
def register(request):
    # Create a filtered list of users that does not include superusers/admins
    users = list(User.objects.filter(is_superuser=False))

    if request.method == 'POST':
        # Create the form object
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            # Form is validated by pre-made Django rules

            # Save the user's information from the form
            user = form.save(commit=False)

            if len(users) > 0:
                # Only check the invite code if a primary user already exists

                # Fetch the inputted invite code from the form
                input_invite_code = request.POST["invite-code"]

                if not SecondaryUserCode.objects.filter(code=input_invite_code).exists():
                    # If the inputted invite code does not exist in the database,
                    # then return an error message to the user and redirect them to try again 
                    messages.error(request, "Invalid invite code.")
                    return redirect("authentication:register")
                else:
                    user.save()
            else:
                # If there are no prior users, then this new user must be the primary user
                user.is_primary_user = True
                user.save()

                # Create a random 12-digit alphanumeric code to be used to invite secondary members
                SecondaryUserCode.objects.create(primary_user=user, code=uuid.uuid4().hex[:12].upper())

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
        return redirect("authentication:login")
    return HttpResponseNotAllowed(["POST"])