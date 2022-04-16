from django.shortcuts import redirect, render
from django.http import HttpResponse
from usuario.models import Usuario
from .models import Livro

# Create your views here.

def home(request):
    # um condicional para se permitir que o usuario cadastrado entre
    if request.session.get('usuario'):
        # pega o usuario do banco de dados e retorna na tela inicial
        usuario = Usuario.objects.get(id = request.session['usuario'])

        livros = Livro.objects.filter(usuario=usuario)
        return render(request, "home.html", {'livros':livros}) 
    else:
        return redirect("/auth/login/?status=2")


def ver_livro(request, id):
    livro = Livro.objects.get(id = id)
    return render(request, 'ver_livro.html', {'livro': livro})