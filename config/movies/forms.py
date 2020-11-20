from django import forms
from .models import Review, Comment, Oneline


class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        fields = ['title', 'content',]


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content',]
        # exclude = ['article', 'user',]


class OnelineForm(forms.ModelForm):

    class Meta:
        model = Oneline
        fields = ['content',]
        # exclude = ['article', 'user',]
