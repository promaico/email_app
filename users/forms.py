from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ValidationError

class RegistrationForm(UserCreationForm):
    
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Es existiert bereits ein Account mit dieser E-Mail!")
        return email
    

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]  
        
        
class Email_Form:
    sender = forms.EmailField(max_length=50, required=True)
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('additional_email', 'additional_password')