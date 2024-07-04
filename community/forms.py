from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('category', 'title', 'content', 'photo', 'hashtags')  # 해시태그 필드 추가
        widgets = {
            'hashtags': forms.TextInput(attrs={'placeholder': '해시태그 입력'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', 'parent',)
        widgets = {
            'parent': forms.HiddenInput()
        }