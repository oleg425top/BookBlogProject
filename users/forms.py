from django import forms


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name , field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserLoginForm(StyleFormMixin, forms.Form):
    email = forms.EmailField()
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
