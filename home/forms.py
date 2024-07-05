from django import forms
from .models import Advice


class AdviceForm(forms.ModelForm):
    class Meta:
        model = Advice
        fields = ['title', 'content', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={'id': 'id_title', 'maxlength': 20}),
            'content': forms.Textarea(attrs={'id': 'id_content', 'maxlength': 500}),
            'photo': forms.ClearableFileInput(attrs={'id': 'id_photo'}),
        }
