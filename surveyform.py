from django.shortcuts import render, redirect
from django import forms

class SurveyForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'}))    #Required
    middle_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your middle name' }))    #optional
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'}))      #Required
    email = forms.EmailField(max_length=50, required=True, widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'}))                      #Required
    country_code = forms.CharField(max_length=5, required=True, widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter country code'}))      #Required
    phone_number = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone no'}))    #Required
    gender = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]
    gender = forms.ChoiceField(
        choices=gender,
        widget=forms.RadioSelect
    )
    favorite_color = [
        ("Red", "Red"),
        ("Violet", "Violet"),
        ("Green", "Green"),
        ("Yellow", "Yellow")
    ]
    favorite_color = forms.ChoiceField(
        choices=favorite_color,
        widget=forms.Select(attrs={"class": "form-control", "id": "genderDropdown"})
    )
    favorite_fruit = [
        ("Watermelon", "Watermelon"),
        ("Papaya", "Papaya"),
        ("Apple", "Apple"),
        ("Tomato", "Tomato"),
    ]
    favorite_fruit = forms.MultipleChoiceField(
        choices=favorite_fruit,
        widget=forms.CheckboxSelectMultiple,
        required=True  # Set to False if selection is optional
    )
    description = forms.CharField(widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Description'}))              #Optional