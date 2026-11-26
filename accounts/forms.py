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
                raise forms.ValidationError('Фото только таких форматов как .jpg or .jpeg.')
            if photo.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Фото не должно быть больше 2МБ.')
        return photo

class RegistrationForm(forms.Form):
    full_name = forms.CharField(
        label='Полное имя',
        required=True,
        validators=[
            RegexValidator(
                regex = r'^[а-яА-ЯёЁ\s-]+$',
                message =  'Введите только русские буквы.'
            )
        ]
    )

    username = forms.CharField(
        label='Логин',
        required=True,
        validators=[
            RegexValidator(
                regex = r'^[A-Za-z][A-Za-z0-9._]*$',
                message = 'Логин должен содержать только буквы, цифры и символы.'
            )
        ]
    )
    email = forms.EmailField(
        label='Электронная почта',
        required=True,
        error_messages={'invalid': 'Неверная электронная почта.'},
    )

    password = forms.CharField(
        label='Пароль',
        required=True,
        widget=forms.PasswordInput,
        error_messages={'invalid': 'Неверный пароль! Попробуй еще раз!.'},
    )

    password_confirmation = forms.CharField(
        label='Повтор пароля',
        required=True,
        widget=forms.PasswordInput,
    )

    consent = forms.BooleanField(
        label = 'Согласие на обработку персональных данных',
        required=True,
        error_messages={'required': 'Сделайте согласие на обработку персональных данных.'},
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Этот пользователь уже есть.')
        return username
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError('Пароль не совпадает.')
        return cleaned_data
