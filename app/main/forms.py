from django import forms
from main.const import KEY_USER_TYPES_CHOICES
from main.models import Recipe

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
    

class LogininForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        required=True,
        max_length=255,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email'
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
    
class AddRecipeModelForm(forms.ModelForm):
    id_category_recipe = forms.IntegerField(
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Recipe
        fields = [
            'title', 
            'html_description', 
            'ingredients', 
            'steps', 
            'time_cooking'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'html_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'steps': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'time_cooking': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }