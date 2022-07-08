from distutils.command.upload import upload
from django.db import models    
from datetime import date
import datetime
from django.db.models.base import Model
from usuario.models import Usuario

class Categoria(models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.TextField()
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.nome
    


class Livro(models.Model):
    img = models.ImageField(upload_to = "capa_livro", null=True, blank=True)
    nome = models.CharField(max_length = 100)
    autor = models.CharField(max_length = 30)
    co_autor = models.CharField(max_length = 30, blank = True, null = True)
    data_cadastro = models.DateField(default = date.today)
    emprestado = models.BooleanField(default = False)      
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

    class Meta:       
        verbose_name = 'Livro'

    # mostrar o nome do livro na tela
    def __str__(self):
        return self.nome



class Emprestimos(models.Model):
    choices = (
        ('P', 'Péssimo'),
        ('R', 'Ruim'),
        ('B', 'Bom'),
        ('O', 'Ótimo')
    )
    nome_emprestado = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, blank = True, null = True)
    nome_emprestado_anonimo = models.CharField(max_length = 30, blank = True, null = True)
    data_emprestimo = models.DateTimeField(default=datetime.datetime.now())
    data_devolucao = models.DateTimeField(blank = True, null = True)  
    livro = models.ForeignKey(Livro, on_delete=models.DO_NOTHING)
    avaliacao = models.CharField(max_length=1, choices=choices, null=True, blank=True)

    def __str__(self)->str:
        return f"{self.nome_emprestado} | {self.livro}"
    