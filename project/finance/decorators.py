from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def primary_user_required(view_function):
    @wraps(view_function)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_primary_user:
            messages.error(request, "Only primary users can perform this action!")
            current_page = request.path.split("/")[2]
            return redirect(f"finance:{current_page}")
        return view_function(request, *args, **kwargs)
    return _wrapped_view