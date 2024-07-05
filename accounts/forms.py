from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    profile_picture = forms.ImageField(required=False)
    date_of_birth_year = forms.ChoiceField(choices=[(year, year) for year in range(1930, 2025)], required=True)
    date_of_birth_month = forms.ChoiceField(choices=[(month, month) for month in range(1, 13)], required=True)
    date_of_birth_day = forms.ChoiceField(choices=[(day, day) for day in range(1, 32)], required=True)
    username = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = CustomUser
        fields = ('profile_picture', 'username', 'password1', 'password2', 'nickname', 'email', 'date_of_birth_year', 'date_of_birth_month', 'date_of_birth_day', 'phone_number')

class EmailVerificationForm(forms.Form):
    email = forms.EmailField()

class VerifyCodeForm(forms.Form):
    code = forms.CharField(max_length=6)