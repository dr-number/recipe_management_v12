from django import forms
from main.const import KEY_USER_TYPES_CHOICES

class CreateAccountForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        required=True,
        max_length=255,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email'
        })
    )
    
    first_name = forms.CharField(
        label='Имя',
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше имя'
        })
    )
    
    last_name = forms.CharField(
        label='Фамилия',
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите вашу фамилию'
        })
    )
    
    password = forms.CharField(
        label='Пароль',
        required=True,
        max_length=255,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )
    
    password2 = forms.CharField(
        label='Подтверждение пароля',
        required=True,
        max_length=255,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        })
    )
    
    type = forms.ChoiceField(
        label='Тип аккаунта',
        required=True,
        choices=KEY_USER_TYPES_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    