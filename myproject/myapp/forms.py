# forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class CustomAuthenticationForm(AuthenticationForm):
    # Add any additional fields or customization if needed
    pass

class CustomUserCreationForm(UserCreationForm):
    # Add any additional fields or customization if needed
    pass
