from django import forms
from .models import Publisher, Game, Review, User, Wishlist

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']  # Only need to input username; join_date will be auto-generated

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['user', 'game', 'rating']  # Fields to input or update
