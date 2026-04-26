from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView
from fnschool import _, count_chinese_characters

from .fntoken import account_activation_token
from .forms import FnuserForm, FnuserLoginForm, FnuserSignUpForm

# Create your views here.

LOGIN_URL = settings.LOGIN_URL


def fnprofile_new(request):
    form = None
    if request.method == "POST":
        form = FnuserSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.username = form.cleaned_data["username"]
            if settings.EMAIL_BACKEND:
                user.is_active = False
            user.save()

            if settings.EMAIL_BACKEND:
                current_site = get_current_site(request)
                mail_subject = _("Activate your account.")
                message = render_to_string(
                    "fnprofile/active_email.html",
                    {
                        "user": user,
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": account_activation_token.make_token(user),
                    },
                )
                to_email = form.cleaned_data.get("email")
                email = EmailMessage(
                    mail_subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    to=[to_email],
                )
                email.send()

                return render(request, "fnprofile/confirm_email.html")
            else:
                login(request, user)
                return redirect("fnhome:home")
    else:
        form = FnuserSignUpForm()

    return render(request, "fnprofile/create.html", {"form": form})


def activate(request, uidb64, token):
    uid = None
    user = None

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Fnuser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, "fnprofile/activation_success.html")
    else:
        return render(request, "fnprofile/activation_invalid.html")


def fnprofile_log_in(request):
    if request.method == "POST":
        form = FnuserLoginForm(request.POST, request=request)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if not user.email_verified:
                    if settings.EMAIL_BACKEND:
                        current_site = get_current_site(request)
                        mail_subject = _("Activate your account.")
                        message = render_to_string(
                            "fnprofile/active_email.html",
                            {
                                "user": user,
                                "domain": current_site.domain,
                                "uid": urlsafe_base64_encode(
                                    force_bytes(user.pk)
                                ),
                                "token": account_activation_token.make_token(
                                    user
                                ),
                            },
                        )
                        to_email = form.cleaned_data.get("email")
                        email = EmailMessage(
                            mail_subject, message, to=[to_email]
                        )
                        email.send()

                        return render(request, "fnprofile/confirm_email.html")

                login(request, user)
                next_url = request.POST.get("next") or reverse_lazy(
                    "fnhome:home"
                )
                return redirect(next_url)
    else:
        form = FnuserLoginForm()

    return render(request, "fnprofile/log_in.html", {"form": form})


def fnprofile_log_out(request):
    logout(request)
    return redirect("fnhome:home")


@login_required
def fnprofile_edit(request):
    form = None
    if request.method == "POST":
        form = FnuserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, _("Your information has been updated successfully!")
            )
            return redirect("fnhome:home")
    else:
        form = FnuserForm(instance=request.user)
    return render(request, "fnprofile/edit.html", {"form": form})


# The end.
