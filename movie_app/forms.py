from django import forms
from .models import Movies, Review


class MovieForm(forms.ModelForm):
    class Meta:
        model=Movies
        fields = ['title', 'poster', 'description', 'release_date', 'actors', 'category', 'youtube_link']
class ReviewForm(forms.ModelForm):

    class Meta:
        model=Review
        fields=['comment','rating']