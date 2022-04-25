from dataclasses import fields
from django import forms
from .models import *


class NotasForm(forms.ModelForm):
    class Meta:
        model = Notas
        fields = ['titulo','descricao']