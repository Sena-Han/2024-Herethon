from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    profile_picture = forms.ImageField(required=False)
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1930, 2025)))
    username = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15)
    national_id = forms.CharField(max_length=7, required=False)

    class Meta:
        model = CustomUser
        fields = ('profile_picture', 'password1', 'password2', 'email', 'username', 'date_of_birth', 'phone_number', 'national_id')

class EmailVerificationForm(forms.Form):
    email = forms.EmailField()

class VerifyCodeForm(forms.Form):
    code = forms.CharField(max_length=6)

