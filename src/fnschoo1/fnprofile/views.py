from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView
from fnschool import _, count_chinese_characters
from fnschool.fncookie import get_object_orders_from_cookie

from .fntoken import account_activation_token
from .forms import FnuserForm, FnuserLoginForm, FnuserSignUpForm
from .models import Fnemail, Fnuser

LOGIN_URL = settings.LOGIN_URL


def new_fnprofile(request):
    if request.user.is_authenticated:
        messages.info(request, _("You are already logged in."))
        return redirect("fnhome:home")

    form = None
    if request.method == "POST":
        form = FnuserSignUpForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                user.set_password(form.cleaned_data["password1"])
                user.username = form.cleaned_data["username"]
                fn_email = Fnemail.objects.get(user=user, is_primary=True)
                if settings.EMAIL_BACKEND:
                    user.is_active = False
                user.save()

                if settings.EMAIL_BACKEND:
                    if send_verification_email(request, user, fn_email):
                        messages.success(
                            request,
                            _(
                                "Registration successful! Verification email sent to {email} ."
                            ).format(email=user.email),
                        )
                    else:
                        messages.warning(
                            request,
                            _(
                                "Registration successful, but verification email failed to send."
                            ),
                        )
                    return render(request, "fnprofile/edit_email.html")
                else:
                    login(request, user)
                    return redirect("fnhome:home")
    else:
        form = FnuserSignUpForm()

    return render(request, "fnprofile/new_profile.html", {"form": form})


def fnprofile_log_in(request):
    if request.method == "POST":
        form = FnuserLoginForm(request, data=request.POST)

        if form.is_valid():
            username = self.cleaned_data.get("username")
            password = self.cleaned_data.get("password")
            if username and password:
                user = Fnuser.objects.filter(username=username).first()
                password_is_incorrect_str = _(
                    "The account does not exist or the password is incorrect!"
                )
                if not user:
                    messages.warning(request, password_is_incorrect_str)
                    form.add_error("username", password_is_incorrect_str)
                else:
                    password_checked = user.check_password(password)
                    if not password_checked:
                        messages.warning(request, password_is_incorrect_str)
                        form.add_error("username", password_is_incorrect_str)
                    else:
                        if (
                            settings.EMAIL_BACKEND
                            and not user.has_verified_email()
                        ):
                            return redirect(
                                reverse(
                                    "fnprofile:edit_email",
                                    kwargs={"email_id": user.get_first_email()},
                                )
                            )
                        else:
                            login(request, user)
                            messages.success(
                                request,
                                _("Welcome back, {username} !").format(
                                    username=user.username
                                ),
                            )
                            next_url = request.POST.get("next") or reverse_lazy(
                                "fnhome:home"
                            )
                            return redirect(next_url)
    else:
        form = FnuserLoginForm(request)

    return render(
        request,
        "fnprofile/fnprofile_log_in.html",
        {"form": form, "EMAIL_BACKEND": settings.EMAIL_BACKEND},
    )


def fnprofile_log_out(request):
    if request.user.is_authenticated:
        messages.info(request, _("You have been logged out"))
    logout(request)
    return redirect("fnhome:home")


@login_required
def edit_fnprofile(request):
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
    return render(request, "fnprofile/edit_fnprofile.html", {"form": form})


@login_required
def list_emails(request):
    emails = Fnemail.objects.filter(user=request.user).order_by(
        "-is_primary", "-is_verified", "-created_at"
    )

    total_count = emails.count()
    verified_count = emails.filter(is_verified=True).count()
    primary_email = emails.filter(is_primary=True, is_active=True).first()

    add_form = FnemailAddForm(user=request.user, request=request)
    bulk_add_form = FnemailBulkAddForm(user=request.user)

    context = {
        "emails": emails,
        "total_count": total_count,
        "verified_count": verified_count,
        "primary_email": primary_email,
        "add_form": add_form,
        "bulk_add_form": bulk_add_form,
        "title": _("My Emails"),
    }

    return render(request, "fnprofile/list_emails.html", context)


@login_required
def new_email(request):
    if request.method == "POST":
        form = FnemailAddForm(request.POST, user=request.user, request=request)

        if form.is_valid():
            try:
                with transaction.atomic():
                    email = form.save(commit=False)
                    email.user = request.user

                    if not Fnemail.objects.filter(
                        user=request.user, is_active=True
                    ).exists():
                        email.is_primary = True

                    email.save()

                    if send_verification_email(request, request.user):
                        messages.success(
                            request,
                            _(
                                "Email added successfully! Verification email sent."
                            ),
                        )
                        logger.info(
                            f"User {request.user.username} added email: {email.email}"
                        )
                    else:
                        messages.warning(
                            request,
                            _(
                                "Email added, but verification email failed to send."
                            ),
                        )

                    return redirect("email_list")

            except Exception as e:
                logger.error(f"Failed to add email: {e}", exc_info=True)
                messages.error(
                    request, _("Failed to add email. Please try again.")
                )
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = FnemailAddForm(user=request.user, request=request)

    context = {
        "form": form,
        "title": _("Add Email"),
    }

    return render(request, "fnprofile/new_email.html", context)


@login_required
def view_email(request, email_id):
    email = get_object_or_404(Fnemail, id=email_id, user=request.user)
    verification_form = FnemailVerificationForm()

    can_resend = email.can_resend_verification()
    if email.verification_sent_at:
        seconds_since = (
            timezone.now() - email.verification_sent_at
        ).total_seconds()
        next_resend = max(0, 60 - int(seconds_since))
    else:
        next_resend = 0

    context = {
        "email": email,
        "verification_form": verification_form,
        "can_resend": can_resend,
        "next_resend": next_resend,
        "title": _("Email Details"),
    }

    return render(request, "fnprofile/view_email.html", context)


def edit_email(request, email_id):
    email = Fnemail.objects.filter(pk=email_id).first()
    if not email:
        return

    user = email.user
    if not user:
        return

    if request.method == "POST":
        form = FnemailEditForm(request.POST, instance=email)

        if form.is_valid():

            is_verified = form.cleaned_data.get("is_verified")
            if not is_verified:
                if form.instance.send_verification_email():
                    messages.success(request, _("Email set as primary"))
                else:
                    from .models import resend_verification_email_time_interval
                    form.add_error({"is_verified":_("The verification email failed to be sent. Please wait for {time_interval} seconds and try again!").format(time_interval=resend_verification_email_time_interval)})
            else:
                if form.cleaned_data.get("is_primary"):
                    messages.success(request, _("Email set as primary"))
                else:
                    messages.success(request, _("Email settings updated"))
                
                form.save()

                return redirect(
                    reverse(
                        "fnprofile:email_detail", kwargs={"email_id": email_id}
                    )
                )

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = FnemailEditForm(instance=email)

    context = {
        "form": form,
        "email": email,
    }

    return render(request, "fnprofile/edit_email.html", context)


@login_required
def delete_email(request, email_id):
    if request.method != "POST":
        return redirect("email_list")
    email = get_object_or_404(Fnemail, id=email_id, user=request.user)

    try:
        if email.is_primary:
            messages.error(request, _("Cannot delete primary email"))
            return redirect("email_list")

        email_email = email.email
        email.delete()

        messages.success(request, _("Email deleted"))
        logger.info(
            f"User {request.user.username} deleted email: {email_email}"
        )

    except Exception as e:
        logger.error(f"Failed to delete email: {e}")
        messages.error(request, _("Failed to delete email"))

    return redirect(reverse("fnprofile:list_emails"))


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")


# The end.
