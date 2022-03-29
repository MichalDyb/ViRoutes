from django import forms
from django.core.validators import RegexValidator

class SendEmailForm(forms.Form):
    name = forms.CharField(label='Imię:', required=True, max_length=50)
    fromEmail = forms.EmailField(label='Email:', required=True)
    message = forms.CharField(label='Wiadomość:', required=True, widget=forms.widgets.Textarea)