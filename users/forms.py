from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name , field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserLoginForm(StyleFormMixin, forms.Form):
    email = forms.EmailField()
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'})
    )
    first_name = forms.CharField(
        label='Имя',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    image = forms.ImageField(
        label='Аватар',
        required=False,  # Необязательное поле
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )
    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'image', 'password1', 'password2')
