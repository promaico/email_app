from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.urls import reverse
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.decorators import login_required

# Create your views here.



def register_user(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = "Aktivieren sie ihren Account"
            message = render_to_string("registration/account_activation_email.html", {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user)
            })
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, "Bitte prüfen sie ihre E-Mail, um die Registrierung abzuschließen.")
            return redirect("index")

    return render(request, "registration/register.html", {"form":form})


def activate(request, uidb64, token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        messages.success(request, "Ihr Account wurde erfolgreich aktiviert")
        return redirect(reverse("login"))
    
    else:
        messages.error(request, "Aktivierungslink ist ungültig oder abgelaufen.")
        return redirect("index")


@login_required
def profile(request):
    render(request, "users/profile.html")

def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user is not None:
                form = LoginForm()
                login(request, user)
                if user_logged_in():
                    messages.success(request, "Sie haben sich erfolgreich eingeloggt!")  # Display login success message
                    return redirect("users-profile")
                else:
                    messages.error(request, "Fehler beim Einloggen. Bitte überprüfen Sie Ihre Anmeldeinformationen.")  # Display login error message
    return render(request, "registration/login.html", {"form": form})

def logout(request):
    logout(request)
    if user_logged_out():
        messages.success(request, "Sie wurden erfolgreich ausgeloggt!")  # Display logout success message
        return redirect("index")
    else:
        messages.error(request, "Fehler beim Ausloggen. Bitte versuchen Sie es erneut.")  # Display logout error message


def index(request):
    messages_to_display = messages.get_messages(request)

    return render(request, "index.html", {"messages": messages_to_display} )


