from functools import wraps

from django.contrib.auth.decorators import login_required as _login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect


def student_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        decorated = _login_required(lambda req: req)
        result = decorated(request)
        if isinstance(result, HttpResponseRedirect):
            return result

        if not hasattr(request.user, "student_profile"):
            return redirect("education:edit_student_profile")

        return view_func(request, *args, **kwargs)

    return wrapper


def teacher_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        decorated = _login_required(lambda req: req)
        result = decorated(request)
        if isinstance(result, HttpResponseRedirect):
            return result

        if not hasattr(request.user, "teacher_profile"):
            return redirect("education:edit_teacher_profile")

        return view_func(request, *args, **kwargs)

    return wrapper


# The end.
