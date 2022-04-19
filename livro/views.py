from django.shortcuts import redirect, render
from django.http import HttpResponse
from usuario.models import Usuario
from .models import Livro, Categoria, Emprestimos
from .forms import CadastroLivro

# Create your views here.

def home(request):
    # um condicional para se permitir que o usuario cadastrado 
    if request.session.get('usuario'):
        # pega o usuario do banco de dados e retorna na tela inicial
        usuario = Usuario.objects.get(id = request.session['usuario'])
        livros = Livro.objects.filter(usuario=usuario)
        form = CadastroLivro()
        return render(request, "home.html", {'livros':livros, 
                                'usuario_logado': request.session.get('usuario'), 'form':form}) 
    else:
        return redirect("/auth/login/?status=2")


def ver_livro(request, id):
     # um condicional para se permitir que o usuario cadastrado 
    if request.session.get('usuario'):
        # capturo o id do lirvo
        livro = Livro.objects.get(id = id)
        if request.session.get('usuario') == livro.usuario.id:
            categoria_livro = Categoria.objects.filter(usuario_id = request.session.get('usuario'))
            emprestimos = Emprestimos.objects.filter(livro=livro)
            form = CadastroLivro()
            return render(request, 'ver_livro.html', {'livro': livro, 'categoria_livro': categoria_livro, 
                                                    'emprestimos': emprestimos, 'usuario_logado': request.session.get('usuario'),  'form':form})        
        else:
            return HttpResponse('Você não pode acessar este livro')

    return redirect("/auth/login/?status=2")



def cadastrar_livro(request):
    if request.method == 'POST':
        form = CadastroLivro(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse('Livro Salvo com sucesso')
        else:
            return HttpResponse('DADOS INVÁLIDOS')
            

                
        
