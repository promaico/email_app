from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password1", "password2"]

    def clean_email(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Es existiert bereits ein Account mit diesem Benutzernamen!")
        return username
    

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]  