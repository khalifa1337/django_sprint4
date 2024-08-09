from django import forms
from django.contrib.auth import get_user_model

from .models import Comment, Post

User = get_user_model()


class PostForm(forms.ModelForm):
    """
    Форма для постов на основе модели Post.
    """

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }


class CommentForm(forms.ModelForm):
    """
    Форма для комментариев на основе модели Comment.
    """
    class Meta:
        model = Comment
        fields = ('text',)
