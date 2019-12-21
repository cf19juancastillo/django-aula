"""
    Forms for the descarrega app
"""
from django import forms
from .utils import composa_opcions_grups

class descarregaAlumnesForm(forms.Form):
    grups = forms.CharField(label="Quins grups?",
                           widget=forms.SelectMultiple(
                               choices=composa_opcions_grups()
                               ))


