from pyexpat.errors import messages
from django.shortcuts import render
from .forms import *
from .models import Notas
from django.contrib import messages

# Create your views here.


def home(request):
    return render(request, 'dashboard/home.html')

def notas(request):
    if request.method == 'POST':
        form = NotasForm(request.POST)
        if form.is_valid():
            nota = Notas(
                usuario=request.user,
                titulo=request.POST['titulo'],
                descricao=request.POST['descricao']
                )
            nota.save()
            messages.success(request, f'Nota de {request.user.username} adicionada com Sucesso')
    else:
        form = NotasForm()
    notas = Notas.objects.filter(usuario=request.user)
    context = {'notas':notas,'form':form}
    return render(request, 'dashboard/notes.html', context)