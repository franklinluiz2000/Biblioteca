from django import forms
from django.db.models import fields
from .models import Livro
from django.db import models
from datetime import date
from .models import Categoria

class CadastroLivro(forms.ModelForm):
    
    class Meta:
        model = Livro
        # pode ser escolhido os campos atraves de cada variável de model
        # fields = ('nome','autor', 'co_autor', 'data_cadastro', 'emprestado', 'categoria')
        # passa todos os campos pelo filtro
        fields = "__all__" 
    

''''class CadastroLivro(forms.Form):
    nome = forms.CharField(max_length = 100)
    autor = forms.CharField(max_length = 30)
    co_autor = forms.CharField(max_length = 30)
    data_cadastro = forms.DateField()
    emprestado = forms.BooleanField()      
'''