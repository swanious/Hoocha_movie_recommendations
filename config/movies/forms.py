from django import forms
from .models import Review, Comment, Oneline


class ReviewForm(forms.ModelForm):
    title=forms.CharField(
        label="제목",
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'제목을 작성해주세요.',
            }
        )
    )
    content = forms.CharField(
        label='내용',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': '내용을 작성해주세요.'
            }
        ),
    )

    class Meta:
        model = Review
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content',]


class OnelineForm(forms.ModelForm):
    content = forms.CharField(
        label='한줄평',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '한줄평을 남겨주세요.'
            }
        ),
    )

    RATING_NUMBERS = (
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
        (6,6),
        (7,7),
        (8,8),
        (9,9),
        (10,10),
    )

    vote_rating = forms.IntegerField(
        label='평점',
        widget=forms.Select(
            attrs={
                'class':'form-control'
            },
            choices=reversed(RATING_NUMBERS)
        ),
    )

    class Meta:
        model = Oneline
        fields = ['content', 'vote_rating']

