from functools import wraps

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import RegistrationForm


def site_access_required(view):
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated and not request.session.get("is_guest"):
            return redirect("login")
        return view(request, *args, **kwargs)

    return wrapped


def login_view(request):
    if request.user.is_authenticated or request.session.get("is_guest"):
        return redirect("home")

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        request.session.pop("is_guest", None)
        return redirect("home")

    return render(request, "login.html", {"form": form})


def register_view(request):
    if request.user.is_authenticated or request.session.get("is_guest"):
        return redirect("home")

    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("home")

    return render(request, "register.html", {"form": form})


@require_POST
def guest_view(request):
    request.session["is_guest"] = True
    return redirect("home")


@require_POST
def logout_view(request):
    logout(request)
    return redirect("login")


@site_access_required
def home(request):
    return render(request, "index.html")


@site_access_required
def recipes(request):
    return render(request, "recipes.html")


@site_access_required
def about(request):
    return render(request, "about.html")


@site_access_required
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()
        try:
            validate_email(email)
            valid_email = True
        except ValidationError:
            valid_email = False
        if name and valid_email and message:
            recipient = settings.CONTACT_RECIPIENT_EMAIL
            if not recipient:
                messages.error(request, "Email delivery is not configured. Please set CONTACT_RECIPIENT_EMAIL.")
            else:
                email_message = EmailMessage(
                    subject=f"Recipe site contact from {name}",
                    body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[recipient],
                    reply_to=[email],
                )
                try:
                    email_message.send(fail_silently=False)
                    messages.success(request, "Thank you! Your message was sent successfully.")
                except Exception:
                    messages.error(request, "Your message could not be sent. Please try again later.")
        elif not name or not email or not message:
            messages.error(request, "Please fill in all fields.")
        else:
            messages.error(request, "Please enter a valid email address.")
    return render(request, "contact.html")
