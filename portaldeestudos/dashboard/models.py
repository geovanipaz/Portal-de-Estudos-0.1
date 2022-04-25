from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Notas(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    
    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        
    def __str__(self) -> str:
        return self.titulo