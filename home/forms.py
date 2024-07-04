from django import forms
from .models import Advice


class AdviceForm(forms.ModelForm):
    class Meta:
        model = Advice
        fields = ['title', 'content', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={'maxlength': 20}),
            'content': forms.Textarea(attrs={'maxlength': 500}),
        }
