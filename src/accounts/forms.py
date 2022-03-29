from django import forms
from django.forms import widgets
from django.contrib.auth import authenticate
from .models import User
from mySite import settings
from django.contrib.auth import password_validation

class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label='*Użytkownik:', required=True, max_length=150, validators=[User.username_validator])
    first_name = forms.CharField(label='Imię:', max_length=150, required=False)
    last_name = forms.CharField(label='Nazwisko:', max_length=150, required=False)
    email = forms.EmailField(label='*Email:', required=True)
    password = forms.CharField(label='*Hasło:', required=True, widget=widgets.PasswordInput)
    confirmPassword = forms.CharField(label='*Potwierdź hasło:', required=True, widget=widgets.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirmPassword']

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        confirmPassword = self.cleaned_data.get('confirmPassword')
        username_qs = User.objects.filter(username=username)
        if username_qs.exists():
            raise forms.ValidationError('Podana nazwa użytkownika jest już zajęta.')

        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError('Podany adres email jest już zajęty.')

        if password != confirmPassword:
            raise forms.ValidationError('Podane hasło nie zgadza się z polem potwierdź hasło.')
        try:
            password_validation.validate_password(password, self.instance)
        except forms.ValidationError as error:
            self.add_error('password', error)
        return super(UserRegisterForm, self).clean(*args, **kwargs)

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Użytkownik:', required=True)
    password = forms.CharField(label='Hasło:', required=True, widget=widgets.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Nazwa użytkownika albo hasło nieprawidłowe.')
            if not user.is_active:
                raise forms.ValidationError('Konto tego użytkownika nie jest aktywne.')
            return super(UserLoginForm, self).clean(*args, **kwargs)

class UserChangeEmailForm(forms.Form):
    email = forms.fields.EmailField(label='Nowy email:', required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserChangeEmailForm, self).__init__(*args, **kwargs)

    def clean(self ,*args, **kwargs):
        email = self.cleaned_data['email']

        if email != self.request.user.email:
            email_qs = User.objects.filter(email=email)
            if email_qs.exists():
                raise forms.ValidationError('Podany adres email jest już zajęty.')
        return super(UserChangeEmailForm, self).clean(*args, **kwargs)

class UserChangePasswordForm(forms.Form):
    oldPassword = forms.CharField(label='Stare hasło:', required=True, widget=forms.widgets.PasswordInput)
    newPassword = forms.CharField(label='Nowe hasło:', required=True, widget=forms.widgets.PasswordInput)
    newPasswordConfirm = forms.CharField(label='Potwierdź nowe hasło:', required=True, widget=forms.widgets.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self ,*args, **kwargs):
        oldPassword = self.cleaned_data['oldPassword']
        newPassword = self.cleaned_data['newPassword']
        newPasswordConfirm = self.cleaned_data['newPasswordConfirm']

        user = User.objects.get(username = self.request.user.username)
        if not user.check_password(oldPassword):
            self.add_error('oldPassword', 'Stare hasło jest nie prawidłowe.')

        if newPassword != newPasswordConfirm:
            raise forms.ValidationError('Podane nowe hasło nie zgadza się z polem potwierdź nowe hasło.')
        try:
            password_validation.validate_password(newPassword)
        except forms.ValidationError as error:
            self.add_error('newPassword', error)
        return super(UserChangePasswordForm, self).clean(*args, **kwargs)

class UserChangePersonalDataForm(forms.Form):
    first_name = forms.fields.CharField(label='Imię:', max_length=150, required=False)
    last_name = forms.fields.CharField(label='Nazwisko:', max_length=150, required=False)