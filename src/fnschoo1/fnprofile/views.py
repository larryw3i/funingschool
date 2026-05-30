import logging
from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView
from fnschool import _
from fnschool.views import (
    get_object_orders_from_cookie,
    get_search_params_from_cookie,
)

from .fntoken import account_activation_token
from .forms import (
    FnemailAddForm,
    FnemailDeleteForm,
    FnemailEditForm,
    FnuserForm,
    FnuserLoginForm,
    FnuserSetPasswordForm,
    FnuserSignUpForm,
)
from .models import Fnemail, Fnuser, resend_verification_email_time_interval

logger = logging.getLogger(__name__)
LOGIN_URL = settings.LOGIN_URL


def login(request, user):
    user_login = auth_login(request, user)
    if settings.AS_SITE:
        user.send_login_notification_email(request)
    return user_login


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
                user.save()
                fn_email = Fnemail.objects.filter(
                    user=user, is_primary=True
                ).first()
                if settings.AS_SITE:
                    if fn_email.send_verification_email(request):
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
                    return redirect("fnprofile:edit_email", fn_email.id)
                else:
                    login(request, user)
                    return redirect("fnhome:home")
    else:
        form = FnuserSignUpForm(request=request)

    return render(request, "fnprofile/profile/new.html", {"form": form})


def fnprofile_log_in(request):
    form = None
    context = {}

    if request.method == "POST":
        form = FnuserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data.get("remember_me")
            if username and password:
                user = (
                    Fnuser.objects.filter(email=username).first()
                    if "@" in username
                    else Fnuser.objects.filter(username=username).first()
                )
                password_is_incorrect_str = _(
                    "The account does not exist or the password is incorrect!"
                )
                password_checked = (
                    user.check_password(password) if user else False
                )
                if not user or not password_checked:
                    messages.warning(request, password_is_incorrect_str)
                    form.add_error("username", password_is_incorrect_str)

                elif settings.AS_SITE and not user.has_verified_email():
                    email = user.get_first_email()
                    form_email = form.cleaned_data.get("email", "") or None

                    if email:
                        email_id = email.id
                        return redirect("fnprofile:edit_email", email_id)

                    if form_email:
                        email = Fnemail.objects.create(
                            user=user,
                            email=form_email,
                            is_primary=True,
                        )
                        email_id = email.id
                        return redirect("fnprofile:edit_email", email_id)

                    context.update({"show_email_field": True})
                    form.add_error(
                        "email",
                        _(
                            "Please enter an email address to verify your account!"
                        ),
                    )

                else:
                    login(request, user)
                    if not remember_me:
                        request.session.set_expiry(0)
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

    context.update({"form": form})
    return render(
        request,
        "fnprofile/profile/log_in.html",
        context,
    )


def fnprofile_log_out(request):
    logout_token = request.GET.get("logout_token", None)
    if logout_token:
        user_id_r = request.GET.get("user_id", None)
        if not user_id_r:
            return HttpResponse("Not Found", status=404)
        user_id = force_str(urlsafe_base64_decode(user_id_r))
        user = get_object_or_404(Fnuser, pk=user_id)
        user_sessions = []
        for session in Session.objects.filter(expire_date__gte=timezone.now()):
            session_data = session.get_decoded()
            if session_data.get("_auth_user_id") == str(user.id):
                user_sessions.append(session)
        for session in user_sessions:
            session.delete()
        messages.info(request, _("You account has been loged out."))
        user.logout_token = None
        user.save(update_fields=["logout_token"])
        return redirect("fnhome:home")

    if request.user.is_authenticated:
        messages.info(request, _("You have been logged out"))
    logout(request)
    return redirect("fnhome:home")


def edit_fnprofile(request):
    form = None
    reset_password = request.GET.get("reset_password", None)
    if reset_password and request.user.is_authenticated:
        user = request.user
        if not user.send_reset_password_email(request):
            return HttpResponse("Not Found", status=404)
        messages.info(
            request,
            _(
                "A password reset email has been sent to your email address. Please reset your password according to the instructions in the email."
            ),
        )

        return redirect(
            request.GET.get("next", None) or "fnprofile:edit_profile"
        )

    reset_password_token = request.GET.get("reset_password_token", None)
    if reset_password_token:
        user_id_r = request.GET.get("user_id", None)
        user_id = force_str(urlsafe_base64_decode(user_id_r))
        print(user_id)
        if not user_id:
            return HttpResponse("Not Found", status=404)
        user = get_object_or_404(Fnuser, pk=user_id)
        if request.method == "POST":
            form = FnuserSetPasswordForm(user, request.POST)
            if form.is_valid():
                if not user.verify_reset_password_token(reset_password_token):
                    return HttpResponse("Not Found", status=404)

                password = form.cleaned_data["new_password1"]
                user.reset_password_token = None
                user.set_password(password)
                user.save()
                messages.success(request, _("Your password has been reset."))
                login(request, user)
                return redirect("fnhome:home")

        if not user.verify_reset_password_token(reset_password_token):
            return HttpResponse("Not Found", status=404)
        reset_password_token = user.generate_reset_password_token()
        current_site = get_current_site(request)
        reset_password_url = (
            request.scheme
            + "://"
            + current_site.domain
            + reverse("fnprofile:edit_profile")
            + "?user_id="
            + user_id_r
            + "&reset_password_token="
            + reset_password_token
        )

        form = FnuserSetPasswordForm(user)
        return render(
            request,
            "fnprofile/profile/set_password.html",
            {
                "form": form,
                "user": user,
                "reset_password_url": reset_password_url,
            },
        )

    if not request.user.is_authenticated:
        return HttpResponse("Not Found", status=404)

    if request.method == "POST":
        form = FnuserForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            password = None
            if settings.AS_SITE:
                password = cleaned_data["password"]
                password_confirm = cleaned_data["password_confirm"]
                if (
                    password_confirm
                    and password_confirm
                    and password != password_confirm
                ):
                    form.add_error(
                        "password_confirm", _("Passwords do not match.")
                    )

            user = form.save(commit=False)
            if settings.AS_SITE and password:
                user.set_password(password)
            user.save()
            messages.success(
                request, _("Your information has been updated successfully!")
            )
            return redirect("fnprofile:edit_profile")
    else:
        form = FnuserForm(instance=request.user)
    return render(request, "fnprofile/profile/edit.html", {"form": form})


@login_required
def list_emails(request):
    emails = Fnemail.objects.filter(user=request.user).order_by(
        "-is_primary", "-is_verified", "-created_at"
    )

    total_count = emails.count()
    verified_count = emails.filter(is_verified=True).count()
    primary_email = emails.filter(is_primary=True, is_disabled=False).first()

    for email in emails:
        email.verified_at = email.verified_at_t
    context = {
        "emails": emails,
        "total_count": total_count,
        "verified_count": verified_count,
        "primary_email": primary_email,
    }

    return render(request, "fnprofile/fnemail/list.html", context)


@login_required
def new_email(request):
    user = request.user
    if request.method == "POST":
        form = FnemailAddForm(request.POST, request=request)
        if form.is_valid():
            try:
                with transaction.atomic():

                    email = form.save(commit=False)
                    email.user = user
                    email.save()

                    if email.send_verification_email(request):
                        messages.info(
                            request,
                            _(
                                "Email added successfully! Verification email sent."
                            ),
                        )
                        return render(
                            request,
                            "close.html",
                        )

                    else:
                        messages.error(
                            request,
                            _(
                                "Email added, but verification email failed to send."
                            ),
                        )

            except Exception as e:
                print(e)
                form.add_error(
                    "email", _("Failed to add email. Please try again.")
                )
    else:
        form = FnemailAddForm(request=request)

    context = {
        "form": form,
    }

    return render(request, "fnprofile/fnemail/new.html", context)


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

    return render(request, "fnprofile/fnemail/view.html", context)


def edit_email(request, email_id):
    email = Fnemail.objects.filter(pk=email_id).first()
    if not email:
        return HttpResponse("Not Found", status=404)

    email_address = email.email
    email_is_verified = email.is_verified
    email_user = email.user

    verification_sent_str = _(
        "A verification email has been sent to your email address. Please follow the instructions in the email to complete the verification process."
    )

    verification_sent_unsuccessfully_str = _(
        "The verification email failed to be sent. Please wait for {time_interval} seconds and try again!"
    ).format(time_interval=resend_verification_email_time_interval)

    form = None
    include_document = request.GET.get("include_document", "1") == "1"
    context = {}
    if settings.AS_SITE:
        if not email_user:
            messages.error(request, _("An unknown error has occurred!"))
            return HttpResponse("Not found", status=404)
        elif email_is_verified:
            pass
        elif request.method == "GET":
            token = request.GET.get("verification_token", None)
            if token:
                if email.verification_token_startswith_underline():
                    if not email.verify(token):
                        return HttpResponse("Not Found", status=404)
                    verification_token = email.generate_verification_token(
                        with_underline=False
                    )
                    full_path = (
                        request.get_full_path().split("?")[0]
                        + "?verification_token="
                        + verification_token
                    )
                    return render(
                        request,
                        "fnprofile/fnemail/verify.html",
                        {
                            "full_path": full_path,
                            "username": email_user.username,
                            "email": email_address,
                        },
                    )

                elif email.verify(token):
                    messages.success(request, _("Email verified successfully!"))
                    if not request.user.is_authenticated:
                        login(request, email_user)
                    return redirect(
                        request.GET.get(
                            "next", reverse("fnprofile:list_emails")
                        )
                    )
                else:
                    messages.error(
                        request,
                        _("Token verification failed! Please try again later!"),
                    )
                return redirect(request.path)

            elif request.user.is_authenticated:
                if not request.user == email_user:
                    messages.error(
                        request,
                        _("Please check if your email address is correct!"),
                    )
                    return redirect(request.path)
                resend_verification_email = request.GET.get(
                    "resend_verification_email", "0"
                )
                if resend_verification_email == "1":
                    if email.send_verification_email(request):
                        messages.info(request, verification_sent_str)
                    else:
                        messages.warning(
                            request, verification_sent_unsuccessfully_str
                        )
                    return redirect("fnprofile:list_emails")
                else:
                    pass
            else:
                pass

        elif request.method == "POST":
            form = FnemailEditForm(
                request.POST, instance=email, request=request
            )
            if not form.is_valid():
                pass
            elif not form.cleaned_data["email"] == email_address:
                form.add_error("email", _("An unknown error has occurred!"))
            elif email.send_verification_email(request):
                form.add_error("email", verification_sent_str)
            else:
                form.add_error(
                    "is_verified",
                    verification_sent_unsuccessfully_str,
                )
        else:
            pass

    if not form:
        if request.method == "POST":
            form = FnemailEditForm(
                request.POST, request=request, instance=email
            )
            if not form.is_valid():
                pass

            if not request.user.is_authenticated:
                messages.info(
                    request, _("Please log in to change your information.")
                )
                return redirect("fnprofile:log_in")
            elif not email_user == request.user:
                form.add_error(_("An error occurred while saving the form!"))
            elif not form.cleaned_data["email"] == email_address:
                form.add_error("email", _("an unknown error has occurred!"))
            elif (
                form.cleaned_data["is_primary"] == False
                and len(request.user.get_enabled_emails()) == 1
            ):
                form.add_error(
                    "is_primary",
                    _(
                        "You only have one primary email, so you cannot cancel this option."
                    ),
                )

            else:
                if form.cleaned_data["is_primary"]:
                    for _email in request.user.emails.all():
                        _email.is_primary = False
                        _email.save(update_fields=["is_primary"])
                    form.instance.is_disabled = False
                email = form.save(commit=False)
                email.save(update_fields=["is_disabled", "is_primary"])
                if not email.is_primary and form.cleaned_data.get("is_primary"):
                    messages.success(request, _("Email set as primary"))
                else:
                    messages.success(request, _("Email settings updated"))

                if not include_document:
                    return render(request, "close.html")
                return redirect("fnprofile:list_emails")
        else:
            form = FnemailEditForm(instance=email, request=request)

    username = form.instance.user.username
    username = (
        (username[0] + "*" * 5 + username[-1])
        if not request.user.is_authenticated
        else username
    )
    context.update({"form": form, "email": email, "username": username})

    if include_document:
        return render(
            request, "fnprofile/fnemail/edit__document__.html", context
        )
    return render(request, "fnprofile/fnemail/edit__content__.html", context)


@login_required
def delete_email(request, email_id):
    form = None
    email = get_object_or_404(Fnemail, id=email_id, user=request.user)
    if request.method == "POST":
        try:
            if email.is_primary:
                messages.error(request, _("Cannot delete primary email"))
                pass
            else:
                email_address = email.email
                email.delete()
                messages.success(
                    request,
                    _("Email ({email_address}) deleted").format(
                        email_address=email_address
                    ),
                )
                pass

        except Exception as e:
            messages.error(request, _("Failed to delete email."))
        return render(request, "close.html")

    else:
        email.is_primary = email.is_primary_t
        email.is_verified = email.is_verified_t
        email.is_disabled = email.is_disabled_t
        form = FnemailDeleteForm(instance=email)

    return render(request, "fnprofile/fnemail/delete.html", {"form": form})


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")


# The end.
