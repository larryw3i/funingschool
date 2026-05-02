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

# Create your views here.

LOGIN_URL = settings.LOGIN_URL


def send_verification_email(request, user, fn_email=None):
    try:
        fn_email_cp = fn_email
        fn_email = fn_email or Fnemail.objects.get(email=user.email)
        token = fn_email.generate_verification_token()
        current_site = get_current_site(request)
        mail_subject = _("Activate your account.")
        message = render_to_string(
            "fnprofile/active_email.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": token,
            },
        )
        to_email = fn_email.email
        email = EmailMessage(
            mail_subject,
            message,
            from_email=settings.EMAIL_HOST_USER,
            to=[to_email],
        )
        email.send()
        return True
    except Exception as e:
        print(e)
        return False
    pass


def fnprofile_new(request):
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
                                "Registration successful! Verification email sent to {}."
                            ).format(user.email),
                        )
                        logger.info(
                            f"New user registered: {user.username}, email: {user.email}"
                        )
                    else:
                        messages.warning(
                            request,
                            _(
                                "Registration successful, but verification email failed to send."
                            ),
                        )
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

    fn_email = Fnemail.objects.get(email=user.email)
    if user is not None and fn_email.verify(token):
        login(request, user)
        return render(request, "fnprofile/activation_success.html")
    else:
        return render(request, "fnprofile/activation_invalid.html")


def fnprofile_log_in(request):
    if request.method == "POST":
        form = FnuserLoginForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if not Fnemail.objects.filter(
                    user=user, is_primary=True, is_verified=True
                ).exists():
                    fn_email = Fnemail.objects.filter(
                        user=user, is_primary=True
                    ).first()
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
                                "token": fn_email.generate_verification_token(),
                            },
                        )
                        to_email = form.cleaned_data.get("email")
                        email = EmailMessage(
                            mail_subject, message, to=[to_email]
                        )
                        email.send()
                        send_verification_email(request, user)

                        return render(request, "fnprofile/confirm_email.html")

                login(request, user)
                messages.success(
                    request, _("Welcome back, {}!").format(user.username)
                )
                next_url = request.POST.get("next") or reverse_lazy(
                    "fnhome:home"
                )
                return redirect(next_url)
    else:
        form = FnuserLoginForm(request)

    return render(
        request,
        "fnprofile/log_in.html",
        {"form": form, "EMAIL_BACKEND": settings.EMAIL_BACKEND},
    )


def fnprofile_log_out(request):
    if request.user.is_authenticated:
        messages.info(request, _("You have been logged out"))
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


@login_required
def email_list(request):
    """
    List all user emails
    """
    # Get all user emails
    emails = Fnemail.objects.filter(user=request.user).order_by(
        "-is_primary", "-is_verified", "-created_at"
    )

    # Statistics
    total_count = emails.count()
    verified_count = emails.filter(is_verified=True).count()
    primary_email = emails.filter(is_primary=True, is_active=True).first()

    # Forms
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

    return render(request, "fnprofile/email_list.html", context)


@login_required
def email_add(request):
    """
    Add a new email address
    """
    if request.method == "POST":
        form = FnemailAddForm(request.POST, user=request.user, request=request)

        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create email
                    email = form.save(commit=False)
                    email.user = request.user

                    # If first email, set as primary
                    if not Fnemail.objects.filter(
                        user=request.user, is_active=True
                    ).exists():
                        email.is_primary = True

                    email.save()

                    # Send verification email
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
            # Show errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = FnemailAddForm(user=request.user, request=request)

    context = {
        "form": form,
        "title": _("Add Email"),
    }

    return render(request, "fnprofile/email_add.html", context)


@login_required
def email_bulk_add(request):
    """
    Bulk add email addresses
    """
    if request.method == "POST":
        form = FnemailBulkAddForm(request.POST, user=request.user)

        if form.is_valid():
            emails = form.cleaned_data["emails"]
            added_count = 0
            failed_count = 0

            with transaction.atomic():
                for email_address in emails:
                    try:
                        # Create email
                        email = Fnemail.objects.create(
                            user=request.user,
                            email=email_address,
                        )

                        # Send verification email
                        send_verification_email(request, request.user, email)
                        added_count += 1

                    except Exception as e:
                        logger.error(
                            f"Failed to add email {email_address}: {e}"
                        )
                        failed_count += 1

            if added_count > 0:
                messages.success(
                    request,
                    _(
                        "Successfully added {} email(s). Verification emails sent."
                    ).format(added_count),
                )

            if failed_count > 0:
                messages.warning(
                    request,
                    _("Failed to add {} email(s).").format(failed_count),
                )

            return redirect("email_list")
        else:
            # Show errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = FnemailBulkAddForm(user=request.user)

    context = {
        "form": form,
        "title": _("Bulk Add Emails"),
    }

    return render(request, "fnprofile/email_bulk_add.html", context)


@login_required
def email_detail(request, email_id):
    """
    Email detail view
    """
    # Get email, ensure it belongs to current user
    email = get_object_or_404(Fnemail, id=email_id, user=request.user)

    # Verification form
    verification_form = FnemailVerificationForm()

    # Check if can resend verification
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

    return render(request, "fnprofile/email_detail.html", context)


@login_required
def email_edit(request, email_id):
    """
    Edit email settings (mainly set as primary)
    """
    # Get email, ensure it belongs to current user
    email = get_object_or_404(Fnemail, id=email_id, user=request.user)

    if request.method == "POST":
        form = FnemailEditForm(request.POST, instance=email)

        if form.is_valid():
            try:
                form.save()

                if form.cleaned_data.get("is_primary"):
                    messages.success(request, _("Email set as primary"))
                else:
                    messages.success(request, _("Email settings updated"))

                return redirect("email_detail", email_id=email_id)

            except Exception as e:
                logger.error(f"Failed to update email: {e}")
                messages.error(request, _("Failed to update email"))
        else:
            # Show errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = FnemailEditForm(instance=email)

    context = {
        "form": form,
        "email": email,
        "title": _("Edit Email"),
    }

    return render(request, "fnprofile/email_edit.html", context)


@login_required
def email_verify(request, email_id, token=None):
    """
    Verify email address
    """
    # Get email, ensure it belongs to current user
    email = get_object_or_404(Fnemail, id=email_id, user=request.user)

    # If already verified, redirect
    if email.is_verified:
        messages.info(request, _("Email is already verified"))
        return redirect("email_detail", email_id=email_id)

    # Handle URL token (from email link)
    if token:
        if email.verify(token):
            messages.success(request, _("Email verified successfully!"))
            logger.info(
                f"User {request.user.username} verified email: {email.email}"
            )
        else:
            messages.error(request, _("Invalid or expired verification link"))

        return redirect("email_detail", email_id=email_id)

    # Handle form submission (manual token entry)
    if request.method == "POST":
        form = FnemailVerificationForm(request.POST)

        if form.is_valid():
            token = form.cleaned_data["token"]

            if email.verify(token):
                messages.success(request, _("Email verified successfully!"))
                logger.info(
                    f"User {request.user.username} verified email: {email.email}"
                )
            else:
                messages.error(request, _("Invalid verification code"))

            return redirect("email_detail", email_id=email_id)
        else:
            # Show errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = FnemailVerificationForm()

    context = {
        "form": form,
        "email": email,
        "title": _("Verify Email"),
    }

    return render(request, "fnprofile/email_verify.html", context)


@login_required
def email_resend_verification(request, email_id):
    """
    Resend verification email
    """
    if request.method != "POST":
        return redirect("email_detail", email_id=email_id)

    # Get email, ensure it belongs to current user
    email = get_object_or_404(Fnemail, id=email_id, user=request.user)

    # Check if can resend
    if not email.can_resend_verification():
        messages.error(request, _("Please wait 60 seconds before resending"))
        return redirect("email_detail", email_id=email_id)

    try:
        # Resend verification
        if send_verification_email(request, request.user, email):
            messages.success(request, _("Verification email resent"))
            logger.info(
                f"User {request.user.username} resent verification to: {email.email}"
            )
        else:
            messages.error(request, _("Failed to send verification email"))

    except Exception as e:
        logger.error(f"Failed to resend verification: {e}")
        messages.error(request, _("Failed to resend verification email"))

    return redirect("email_detail", email_id=email_id)


@login_required
def email_toggle_status(request, email_id):
    """
    Toggle email active status
    """
    if request.method != "POST":
        return redirect("email_list")

    # Get email, ensure it belongs to current user
    email = get_object_or_404(Fnemail, id=email_id, user=request.user)

    try:
        if email.is_active:
            # Can't disable primary email
            if email.is_primary:
                messages.error(request, _("Cannot disable primary email"))
            else:
                email.is_active = False
                email.save(update_fields=["is_active"])
                messages.success(request, _("Email disabled"))
                logger.info(
                    f"User {request.user.username} disabled email: {email.email}"
                )
        else:
            email.is_active = True
            email.save(update_fields=["is_active"])
            messages.success(request, _("Email enabled"))
            logger.info(
                f"User {request.user.username} enabled email: {email.email}"
            )

    except Exception as e:
        logger.error(f"Failed to toggle email status: {e}")
        messages.error(request, _("Failed to update email status"))

    return redirect("email_list")


@login_required
def email_set_primary(request, email_id):
    """
    Set email as primary
    """
    if request.method != "POST":
        return redirect("email_list")

    # Get email, ensure it belongs to current user
    email = get_object_or_404(Fnemail, id=email_id, user=request.user)

    try:
        email.set_as_primary()
        messages.success(request, _("Email set as primary"))
        logger.info(
            f"User {request.user.username} set primary email: {email.email}"
        )

    except ValidationError as e:
        messages.error(request, str(e))
    except Exception as e:
        logger.error(f"Failed to set primary email: {e}")
        messages.error(request, _("Failed to set primary email"))

    return redirect("email_list")


@login_required
def email_delete(request, email_id):
    """
    Delete email address
    """
    if request.method != "POST":
        return redirect("email_list")

    # Get email, ensure it belongs to current user
    email = get_object_or_404(Fnemail, id=email_id, user=request.user)

    try:
        # Can't delete primary email
        if email.is_primary:
            messages.error(request, _("Cannot delete primary email"))
            return redirect("email_list")

        # Delete email
        email_email = email.email
        email.delete()

        messages.success(request, _("Email deleted"))
        logger.info(
            f"User {request.user.username} deleted email: {email_email}"
        )

    except Exception as e:
        logger.error(f"Failed to delete email: {e}")
        messages.error(request, _("Failed to delete email"))

    return redirect("email_list")


def get_client_ip(request):
    """
    Get client IP address
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")


# The end.
