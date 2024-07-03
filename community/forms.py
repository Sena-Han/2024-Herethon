from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('category', 'title', 'content', 'photo')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', 'parent',)
        widgets = {
            'parent': forms.HiddenInput()
        }