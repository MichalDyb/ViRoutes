from dataclasses import fields
from random import choices
from tabnanny import verbose
from django import forms
from .models import Comment, Route, RouteRate

class AddRouteForm(forms.ModelForm):
    is_published = forms.ChoiceField(label='Opublikować', required=True, 
        help_text='Opublikowanie trasy wiąże się z udostępnieniem jej innym użytkownikom'
            + ' i zablokowaniem edycji trasy.', choices=((False, 'Nie'), (True, 'Tak')))
    class Meta:
        model = Route
        exclude = ['created_by', 'is_deleted', 'date_published', 'last_modyfied']

class EditRouteFullForm(forms.ModelForm):
    is_published = forms.ChoiceField(label='Opublikować', required=True, 
    help_text='Opublikowanie trasy wiąże się z udostępnieniem jej innym użytkownikom'
        + ' i zablokowaniem edycji trasy.', choices=((False, 'Nie'), (True, 'Tak')))
    class Meta:
        model = Route
        exclude = ['created_by', 'is_deleted', 'date_published', 'last_modyfied']

class EditRouteForm(forms.ModelForm):
    class Meta:
        model = Route
        exclude = ['url', 'is_published', 'created_by', 'is_deleted', 'date_published', 'last_modyfied']

class RouteRateForm(forms.ModelForm):
    class Meta:
        model=RouteRate
        fields = ['rate']

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['content']

class SearchForm(forms.Form):
    name = forms.CharField(label='Nazwa trasy:', required=False, max_length=150)
    author = forms.CharField(label='Autor trasy:', required=False, max_length=150)
    date = forms.DateField(label='Data publikacji:', required=False, 
        widget=forms.DateInput(attrs={'type': 'date'}))
    datetype = forms.ChoiceField(label='^Data', required=False, 
        choices=((1, 'Młodsza'), (2, 'Starsza')))
    sort = forms.ChoiceField(label='Sortuj według', required=False, 
        choices=((1, 'Daty publikacji'), (2, 'Nazwy trasy'), (3, 'Autora trasy')))
    sorttype = forms.ChoiceField(label='^Typ sortowania', required=False, 
        choices=((1, 'Malejący'), (2, 'Rosnący')))