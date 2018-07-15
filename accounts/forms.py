
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
class RegistrationForm(UserCreationForm):
   email=forms.EmailField(required=True)
   class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2']
class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        exclude=['user','completed']
