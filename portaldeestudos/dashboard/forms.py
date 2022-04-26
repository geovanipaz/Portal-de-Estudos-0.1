from dataclasses import field, fields
from tkinter import Widget
from django import forms
from .models import *


class NotasForm(forms.ModelForm):
    class Meta:
        model = Notas
        fields = ['titulo','descricao']
  
class DateInput(forms.DateInput):
    input_type = 'date'      
class TarefasForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        widgets = {'prazo':DateInput()}
        fields = ['sujeito', 'titulo','descricao','prazo','ja_finalizada']
        
class DashboardForm(forms.Form):
    texto = forms.CharField(max_length=100, label='Entre com sua busca')
    