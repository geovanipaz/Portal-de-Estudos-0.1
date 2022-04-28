from django import views
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('notas', views.notas, name='notas'),
    path('deleta_nota/<pk>', views.deleta_nota, name='deleta_nota'),
    path('detalhe_nota/<pk>', views.notaDetalheView.as_view(), name='detalhe_nota'),
    
    path('tarefas', views.tarefas, name='tarefas'),
    path('update_tarefa/<pk>', views.update_tarefa, name='update_tarefa'),
    path('deleta_tarefa/<pk>', views.deletar_tarefa, name='deleta_tarefa'),
    
    path('youtube', views.youtube, name='youtube'),
    
    path('fazer/', views.fazer, name='fazer'),
    path('update_fazer/<pk>', views.update_fazer, name='update_fazer'),
    path('deleta_fazer/<pk>', views.deleta_fazer, name='deleta_fazer'),
    
    path('livros', views.livros, name='livros'),
    
    path('dicionario/', views.dicionario, name='dicionario'),
    
    path('wiki', views.wiki, name='wiki'),
    
    path('conversao', views.conversao, name='conversao'),
    
    #path('registro', views.registro, name='registro'),
]
