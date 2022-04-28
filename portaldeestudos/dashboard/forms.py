from dataclasses import field, fields
from tkinter import Widget
from xml.dom.minidom import Attr
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

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
    
class FazerForm(forms.ModelForm):
    class Meta:
        model = Fazer
        fields = ['titulo', 'ja_finalizada']
        
class ConversaoForm(forms.Form):
    CHOICES = [('comprimento','Comprimento'), ('massa','Massa')]
    medicao = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    
class ConversaoCompForm(forms.Form):
    CHOICES = [('jarda','Jarda'),('pé','Pé')]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs={'type':'number', 'placeholder':'Entre com o numero'}
    ))
    medida1 = forms.CharField(
        label='', widget=forms.Select(choices=CHOICES)
    )
    medida2 = forms.CharField(
        label='', widget=forms.Select(choices=CHOICES)
    )

class ConversaoMassaForm(forms.Form):
    CHOICES = [('libra','Libra'),('kilograma','Kilograma')]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs={'type':'number', 'placeholder':'Entre com o numero'}
    ))
    medida1 = forms.CharField(
        label='', widget=forms.Select(choices=CHOICES)
    )
    medida2 = forms.CharField(
        label='', widget=forms.Select(choices=CHOICES)
    )
    
class RegistrarUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']