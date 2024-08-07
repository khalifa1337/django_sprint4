from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        # Указываем модель, на основе которой должна строиться форма.
        model = Post
        # Указываем, что надо отобразить все поля.
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }


class CommentForm(forms.ModelForm):

    class Meta:
        # Указываем модель, на основе которой должна строиться форма.
        model = Comment
        # Указываем, что надо отобразить все поля.
        fields = ('text',)

# class CongratulationForm(forms.ModelForm):

#     class Meta:
#         model = Congratulation
#         fields = ('text',)