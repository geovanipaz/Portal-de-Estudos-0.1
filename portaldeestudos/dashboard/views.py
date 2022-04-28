from operator import truediv
from pyexpat.errors import messages
from tkinter.tix import Tree
from django.shortcuts import redirect, render
from .forms import *
from .models import Notas, Tarefa, Fazer
from django.contrib import messages
from django.views.generic import DetailView
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request, 'dashboard/home.html')
@login_required
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
@login_required
def deleta_nota(request, pk):
    Notas.objects.get(id=pk).delete()
    return redirect('notas')


class notaDetalheView(DetailView):
    model = Notas
    context_object_name = 'nota'
    template_name = 'dashboard/notes_detail.html'
@login_required    
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

@login_required
def update_tarefa(request, pk=None):
    tarefa = Tarefa.objects.get(id=pk)
    if tarefa.ja_finalizada == True:
        tarefa.ja_finalizada = False
    else:
        tarefa.ja_finalizada = True
    tarefa.save()
    return redirect('tarefas') 

@login_required
def deletar_tarefa(request, pk=None):
    Tarefa.objects.get(id=pk).delete()
    return redirect('tarefas')
@login_required
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

@login_required
def fazer(request):
    if request.method == 'POST':
        form = FazerForm(request.POST)
        if form.is_valid():
            try:
                finalizada = request.POST['ja_finalizada']
                if finalizada == 'on':
                    finalizada = True
                else:
                    finalizada = False
            except:
                finalizada = False
            titulo = request.POST['titulo']
            fazer = Fazer(
                usuario=request.user,
                titulo=titulo,
                ja_finalizada=finalizada
            )
            fazer.save()
            messages.success(request,f'A fazer Adicionada por {request.user.username}.')
            return redirect('fazer')
    else:
        form  = FazerForm()
    fazer = Fazer.objects.filter(usuario=request.user)
    if len(fazer) == 0:
        fazer_feitos = True
    else:
        fazer_feitos = False
    context = {
        'form':form,
        'fazeres': fazer,
        'fazer_feitos':fazer_feitos,
    }
    return render(request,'dashboard/todo.html', context)
@login_required
def update_fazer(request, pk=None):
    fazer = Fazer.objects.get(id=pk)
    if fazer.ja_finalizada == True:
        fazer.ja_finalizada = False
    else:
        fazer.ja_finalizada = True
    fazer.save()
    return redirect('fazer')
@login_required    
def deleta_fazer(request, pk=None):
    fazer = Fazer.objects.get(id=pk)
    fazer.delete()
    messages.success(request, f'Fazer {fazer.titulo} foi apagada.')
    return redirect('fazer')

@login_required
def livros(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        texto = request.POST['texto']
        url = 'https://www.googleapis.com/books/v1/volumes?q='+texto
        r = requests.get(url)
        answer = r.json()
        resultado_lista = []
        for i in range(10):
            resultado_dict = {
                'titulo':answer['items'][i]['volumeInfo']['title'],
                'subtitulo':answer['items'][i]['volumeInfo'].get('subtitle'),
                'descrição':answer['items'][i]['volumeInfo'].get('description'),
                'quantidade':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categoria':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRatig'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLinks'),
            }
            
           
            resultado_lista.append(resultado_dict)
            context = {
                'form':form,
                'results': resultado_lista,
            }
        return render(request,'dashboard/books.html', context)
    else:
        form = DashboardForm()
    context = {'form':form}
    return render(request, 'dashboard/books.html', context)
@login_required
def dicionario(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        texto = request.POST['texto']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+texto
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics= answer[0]['phonetics'][0]['text']
            audio= answer[0]['phonetics'][0]['audio']
            definition= answer[0]['meanings'][0]['definitions'][0]['definition']
            example= answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms= answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form':form,
                'input':texto,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms': synonyms
            }
        except:
            context = {
                'form':form,
                'input':texto
            }
        return render(request,'dashboard/dictionary.html', context)
    else:
        form = DashboardForm()
        context = {
            'form':form,
        }
    return render(request,'dashboard/dictionary.html', context)
@login_required
def wiki(request):
    if request.method == 'POST':
        texto = request.POST['texto']
        form = DashboardForm(request.POST)
        search = wikipedia.page(texto)
        context = {
            'form':form,
            'search':search.title,
            'link':search.url,
            'details':search.summary
        }
        return render(request, 'dashboard/wiki.html', context)
    else:
        form = DashboardForm()
        context = {
            'form':form,
        
        }
    return render(request,'dashboard/wiki.html', context)
@login_required
def conversao(request):
    if request.method == 'POST':
        form = ConversaoForm(request.POST)
        if request.POST['medicao'] == 'comprimento':
            medicao_form = ConversaoCompForm()
            context = {
                'form':form,
                'm_form': medicao_form,
                'input':True
            }
            if 'input' in request.POST:
                primeiro = request.POST['medida1']
                segundo = request.POST['medida2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if primeiro == 'jarda' and segundo == 'pé':
                        answer = f'{input} jarda = {int(input)*3} pé'
                    if primeiro == 'pé' and segundo == 'jarda':
                        answer = f'{input} pé = {int(input)*3} jarda'
                context = {
                    'form':form,
                    'm_form': ConversaoCompForm,
                    'input': True,
                    'answer':answer
                }
        else:
            if request.POST['medicao'] == 'massa':
                medicao_form = ConversaoMassaForm()
            context = {
                'form':form,
                'm_form': medicao_form,
                'input':True
            }
            if 'input' in request.POST:
                primeiro = request.POST['medida1']
                segundo = request.POST['medida2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if primeiro == 'pound' and segundo == 'kilograma':
                        answer = f'{input} pound = {int(input)*0.453592} kilograma'
                    if primeiro == 'pé' and segundo == 'jarda':
                        answer = f'{input} kilograma = {int(input)*2.2062} pound'
                context = {
                    'form':form,
                    'm_form': ConversaoMassaForm,
                    'input': True,
                    'answer':answer
                }
    else:
        form = ConversaoForm()
        context = {
            'form':form,
            'input':False
        }
    return render(request, 'dashboard/conversion.html', context)

def registro(request):
    if request.method == 'POST':
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Conta Criada por {username}.')
            return redirect('login')
    else:
        
        form = RegistrarUsuarioForm()
    context = {
        'form':form,
    }
    return render(request,'dashboard/register.html', context)
@login_required
def perfil(request):
    tarefas = Tarefa.objects.filter(ja_finalizada=False, usuario=request.user)
    fazer = Fazer.objects.filter(ja_finalizada=False, usuario=request.user)
    if len(tarefas) == 0:
        tarefas_feitas = True
    else: 
        tarefas_feitas = False
    if len(fazer) == 0:
        fazer_feitas = True
    else:
        fazer_feitas = False
    context = {
        'tarefas':tarefas,
        'fazers':fazer,
        'tarefas_feitas': tarefas_feitas,
        'fazer_feitas': fazer_feitas
    }
    return render(request, 'dashboard/profile.html', context)