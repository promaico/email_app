from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm, ProfileForm
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
from imapclient import IMAPClient
import logging
import ssl
import quopri
from dotenv import load_dotenv
import os
from .forms import Email_Form

# Create your views here.

#User Register View
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

#User E-Mail Activation View
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

        messages.success(request, "Ihr Account wurde erfolgreich aktiviert")
        return redirect("first_login_view")
    
    else:
        messages.error(request, "Aktivierungslink ist ungültig oder abgelaufen.")
        return redirect("index")

def profile_creation(request):
    form = ProfileForm
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
        form.save()
        messages.success(request, ('Das Profil wurde erfolgreich erstellt'))
        return redirect("login")
    return render(request, "registration/profile_creation.html", {"form":form})

#Link to Profile View
def profile(request):
    return render(request, "profile.html")

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
                if request.user.is_authenticated():
                    messages.success(request, "Sie haben sich erfolgreich eingeloggt!")  # Display login success message
                    return redirect("profile")
                else:
                    messages.error(request, "Fehler beim Einloggen. Bitte überprüfen Sie Ihre Anmeldeinformationen.")  # Display login error message
    return render(request, "registration/login.html", {"form": form})


#User Login View
def first_login_view(request):
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
                if request.user.is_authenticated():
                    messages.success(request, "Sie haben sich erfolgreich eingeloggt!")  # Display login success message
                    return redirect("profile_creation")
                else:
                    messages.error(request, "Fehler beim Einloggen. Bitte überprüfen Sie Ihre Anmeldeinformationen.")  # Display login error message
    return render(request, "registration/login.html", {"form": form})


#User Logout View
def logout(request):
    logout(request)
    if user_logged_out():
        messages.success(request, "Sie wurden erfolgreich ausgeloggt!")  # Display logout success message
        return redirect("index")
    else:
        messages.error(request, "Fehler beim Ausloggen. Bitte versuchen Sie es erneut.")  # Display logout error message


#Link to Index View
def index(request):
    messages_to_display = messages.get_messages(request)

    return render(request, "index.html", {"messages": messages_to_display} )


#User read E-Mails View
def profile_email(request):
    host = 'imap.gmail.com'
    user =  "tjark.jakob.de@gmail.com"
    password =  "sfwu cbae cfqy tjoj"

    MAILSEARCH = "tjark.schulte@gy-cfg.de"
    FOLDER = "INBOX"

    context1 = []

    logging.basicConfig(
        format='%(asctime)s - %(levelname)s: %(message)s',
        level=logging.INFO
    )

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        with IMAPClient(host, ssl_context=ssl_context) as server:
            server.login(user, password)
            select_info = server.select_folder(FOLDER)


            messages = server.search(['FROM', MAILSEARCH])


            for msgid, data in server.fetch(messages, ['ENVELOPE']).items():
                envelope = data[b'ENVELOPE']
                
                #add info to list
                
                msgid = {
                    "id": msgid,
                    "date": envelope.date,
                    "subject": envelope.subject.decode(),
                }
                
                context1.append(msgid)
                
                
            # Nachrichten abrufen (inklusive BODY[TEXT])
            response = server.fetch(messages, ['BODY[TEXT]'])

            # Nachrichten durchgehen und anzeigen
            for msgid, data in response.items():
                # Entschlüssle den Text aus den Bytes
                decoded_text = quopri.decodestring(data[b'BODY[TEXT]']).decode('utf-8')

                # Zeige den entschlüsselten Text an
                for dict in context1:
                    if dict.get("id") == msgid:
                        dict["content"] = decoded_text
                        
                    

            context = {
                'emails': context1
            }
            

    except Exception as e:
        print(f"Error: {e}")

    
    return render(request, "profile_email.html", context)