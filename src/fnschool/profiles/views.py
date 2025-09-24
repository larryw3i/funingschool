from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# Create your views here.

from django.views.generic import CreateView
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate
from .forms import ProfileForm, ProfileLoginForm


def profile_new(request):
    form = None
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.username = form.cleaned_data["username"]
            user.save()
            login(request, user)
            return redirect("home")
    else:
        form = ProfileForm()

    return render(request, "profiles/create.html", {"form": form})


def profile_log_in(request):
    if request.method == "POST":
        form = ProfileLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get("next", "home")
                return redirect(next_url)
    else:
        form = ProfileLoginForm()
    return render(request, "profiles/log_in.html", {"form": form})


def profile_log_out(request):
    logout(request)
    return redirect("home")


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "profiles/edit.html", {"form": form})


# The end.
