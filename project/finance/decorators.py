from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def primary_user_required(view_function):
    # Allows any financial object addition view function to be wrapped
    @wraps(view_function)
    def _wrapped_view(request, *args, **kwargs): # Pass the arguments of the wrapped function into the wrapped view
        if not request.user.is_primary_user:
            # If the user making the URL request to add the financial object is not the primary user,
            # then redirect the user to the main page of the financial object and display an appropriate error message
            messages.error(request, "Only primary users can perform this action!")
            current_page = request.path.split("/")[2]
            return redirect(f"finance:{current_page}")
        return view_function(request, *args, **kwargs)
    return _wrapped_view


