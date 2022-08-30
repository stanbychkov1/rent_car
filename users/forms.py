from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       UsernameField)
from django import forms

User = get_user_model()


class UserAuthForm(AuthenticationForm):
    username = forms.EmailField(label='E-mail',
                                widget=forms.TextInput(
                                    attrs={'autofocus': True}))


class UserRegistrationForm(UserCreationForm):
    password2 = None

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'language')


class UserForm(forms.ModelForm):

    def __init__(self, disable_fields=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if disable_fields:
            for field in self.fields:
                self.fields[field].disabled = True

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email', 'language',)
