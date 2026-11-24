from functools import wraps

from django.contrib.auth.decorators import login_required as _login_required
from django.shortcuts import redirect


def canteen_manager_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        decorated = _login_required(lambda req: req)
        result = decorated(request)
        if isinstance(result, HttpResponseRedirect):
            return result

        if not hasattr(request.user, "canteen_manager"):
            return redirect("canteen:edit_canteen_manager")

        return view_func(request, *args, **kwargs)

    return wrapper


# The end.
