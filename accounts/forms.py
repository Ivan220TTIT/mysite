import os
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import DesignRequest

class DesignRequestForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ('title', 'description', 'category', 'photo')

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            ext = os.path.splitext(photo.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.bmp']:
                raise forms.ValidationError('Photo must be .jpg or .jpeg.')
            if photo.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Photo must be smaller than 2MB.')
        return photo

class RegistrationForm(forms.Form):
    full_name = forms.CharField(
        label='Full Name',
        required=True,
        validators=[
            RegexValidator(
                regex = r'^[а-яА-ЯёЁ\s-]+$',
                message =  'The full name must contain only Cyrillic letters.'
            )
        ]
    )

    username = forms.CharField(
        label='Username',
        required=True,
        validators=[
            RegexValidator(
                regex = r'^[A-Za-z][A-Za-z0-9._]*$',
                message = 'The username must contain only letters, numbers, dots and underscores.'
            )
        ]
    )
    email = forms.EmailField(
        label='Email',
        required=True,
        error_messages={'invalid': 'Enter a valid email address.'},
    )

    password = forms.CharField(
        label='Password',
        required=True,
        error_messages={'invalid': 'Enter a valid password.'},
    )

    password_confirmation = forms.CharField(
        label='Confirm Password',
        required=True,
        widget=forms.PasswordInput,
    )

    consent = forms.BooleanField(
        label = 'Consent to the processing of personal data',
        required=True,
        error_messages={'required': 'It is necessary to confirm your personal data.'},
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('A user with that username already exists.')
        return username
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data
