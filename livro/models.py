from email.policy import default
import imp
from django.db import models
from datetime import date
from usuario.models import Usuario

class Categoria(models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.TextField()

    def __str__(self) -> str:
        return self.nome
    


class Livro(models.Model):
    nome = models.CharField(max_length = 100)
    autor = models.CharField(max_length = 30)
    co_autor = models.CharField(max_length = 30, blank = True, null = True)
    data_cadastro = models.DateField(default = date.today)
    emprestado = models.BooleanField(default = False)
    nome_emprestado = models.CharField(max_length = 30, blank = True, null = True)
    data_emprestimo = models.DateTimeField(blank = True, null = True)
    data_devolucao = models.DateTimeField(blank = True, null = True)
    tempo_duracao = models.DateField(blank = True, null = True)    
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

    class Meta:       
        verbose_name = 'Livro'

    # mostrar o nome do livro na tela
    def __str__(self):
        return self.nome