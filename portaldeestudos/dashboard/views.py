from pyexpat.errors import messages
from django.shortcuts import redirect, render
from .forms import *
from .models import Notas, Tarefa
from django.contrib import messages
from django.views.generic import DetailView
from youtubesearchpython import VideosSearch
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

def deleta_nota(request, pk):
    Notas.objects.get(id=pk).delete()
    return redirect('notas')

class notaDetalheView(DetailView):
    model = Notas
    context_object_name = 'nota'
    template_name = 'dashboard/notes_detail.html'
    
def tarefas(request):
    if request.method == 'POST':
        form = TarefasForm(request.POST)
        if form.is_valid():
            try:
                finalizado = request.POST['ja_finalizado']
                if finalizado == 'on':
                    finalizado = True
                else:
                    finalizado = False
            except:
                finalizado = False
            tarefa = Tarefa(
                usuario = request.user,
                sujeito = request.POST['sujeito'],
                titulo = request.POST['titulo'],
                descricao = request.POST['descricao'],
                prazo = request.POST['prazo'],
                ja_finalizada = finalizado
            )
            tarefa.save()
            messages.success(request,f'Tarefa Adicionada por {request.user.username}.')
    else:
        form = TarefasForm()
    
    tarefas = Tarefa.objects.filter(usuario=request.user)
    if len(tarefas) == 0:
        tarefa_feita = True
    else:
        tarefa_feita = False
    context = {
        'tarefas':tarefas,
        'tarefa_feita':tarefa_feita,
        'form':form
        }
    return render(request, 'dashboard/homework.html', context)

def update_tarefa(request, pk=None):
    tarefa = Tarefa.objects.get(id=pk)
    if tarefa.ja_finalizada == True:
        tarefa.ja_finalizada = False
    else:
        tarefa.ja_finalizada = True
    tarefa.save()
    return redirect('tarefas') 

def deletar_tarefa(request, pk=None):
    Tarefa.objects.get(id=pk).delete()
    return redirect('tarefas')

def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        texto = request.POST['texto']
        video = VideosSearch(texto, limit=10)
        resultado_lista = []
        for i in video.result()['result']:
            resultado_dict = {
                'input': texto,
                'titulo':i['title'],
                'duração':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'canal':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'publicado':i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            resultado_dict['descrição'] = desc
            resultado_lista.append(resultado_dict)
            context = {
                'form':form,
                'results': resultado_lista,
            }
        return render(request,'dashboard/youtube.html', context)
    else:
        form = DashboardForm()
    context = {'form':form}
    return render(request, 'dashboard/youtube.html', context)