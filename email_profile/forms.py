from django import forms


class Email_Form(forms.Form):
    email_user = forms.EmailField(max_length=30)
    email_pass = forms.PasswordInput()
    sender = forms.EmailField(max_length=30)
    
    