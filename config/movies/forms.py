from django import forms
from .models import MovieReview, MovieReviewComment, MovieOneline


class MovieReviewForm(forms.ModelForm):
    
    class Meta:
        model = MovieReview
        fields = ['title', 'content',]


class MovieReviewCommentForm(forms.ModelForm):

    class Meta:
        model = MovieReviewComment
        fields = '__all__'
        # exclude = ['article', 'user',]


class MovieOnelineForm(forms.ModelForm):

    class Meta:
        model = MovieOneline
        fields = '__all__'
        # exclude = ['article', 'user',]
