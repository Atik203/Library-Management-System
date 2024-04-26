from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    review = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Write your review here'}))
    
    class Meta:
        model = Review
        fields = ['review']
       