
from datetime import date, datetime
from django.shortcuts import redirect, render
from django.http import HttpResponse
from usuario.models import Usuario
from .models import Livro, Categoria, Emprestimos
from .forms import CadastroLivro, CadastroCategoria
from django import forms
from django.db.models import Q

def home(request):
    # um condicional para se permitir que o usuario cadastrado 
    if request.session.get('usuario'):
        # pega o usuario do banco de dados e retorna na tela inicial
        usuario = Usuario.objects.get(id = request.session['usuario'])
        status_categoria = request.GET.get('cadastro_categoria')
        livros = Livro.objects.filter(usuario=usuario)
        total_livros = livros.count()
        form = CadastroLivro()
        # pega o id do usuário
        form.fields['usuario'].initial = request.session['usuario']
        # pega somente a categoria do usuario que está logado no sistema
        form.fields['categoria'].queryset = Categoria.objects.filter(usuario=usuario)
        form_categoria = CadastroCategoria()

        usuarios = Usuario.objects.all()
        livros_emprestar = Livro.objects.filter(usuario = usuario).filter(emprestado = False)
        livros_emprestados = Livro.objects.filter(usuario = usuario).filter(emprestado = True)
        print(livros_emprestados)
        return render(request, "home.html", {'livros':livros, 
                                'usuario_logado': request.session.get('usuario'), 
                                'form':form, 'status_categoria': status_categoria, 
                                'form_categoria': form_categoria, 'usuarios': usuarios,
                                'livros_emprestar': livros_emprestar,'total_livros': total_livros,
                                'livros_emprestados': livros_emprestados}) 
    else:
        return redirect("/auth/login/?status=2")


def ver_livros(request, id):
     # um condicional para se permitir que o usuario cadastrado 
    if request.session.get('usuario'):
        # capturo o id do lirvo
        livro = Livro.objects.get(id = id)

        if request.session.get('usuario') == livro.usuario.id:
            # Pega o usuario do banco de dados e retorna na tela inicial
            usuario = Usuario.objects.get(id = request.session['usuario'])
            
            categoria_livro = Categoria.objects.filter(usuario_id = request.session.get('usuario'))
            emprestimos = Emprestimos.objects.filter(livro=livro)           
            form = CadastroLivro()
            # pega o id do usuário
            form.fields['usuario'].initial = request.session['usuario']
            # pega somente a categoria do usuario que está logado no sistema
            form.fields['categoria'].queryset = Categoria.objects.filter(usuario=usuario)

            form_categoria = CadastroCategoria()

            usuarios = Usuario.objects.all()

            livros_emprestar = Livro.objects.filter(usuario = usuario).filter(emprestado = False)
            livros_emprestados = Livro.objects.filter(usuario = usuario).filter(emprestado = True)

            return render(request, 'ver_livro.html', {'livro': livro, 'categoria_livro': categoria_livro, 
                                                    'emprestimos': emprestimos, 
                                                    'usuario_logado': request.session.get('usuario'),  
                                                    'form':form, 'id_livro': id, 'form_categoria': form_categoria,
                                                    'usuarios':usuarios, 'livros_emprestar': livros_emprestar,
                                                    'livros_emprestados': livros_emprestados})        
        else:
            return HttpResponse('Você não pode acessar este livro')

    return redirect("/auth/login/?status=2")



def cadastrar_livro(request):
    if request.method == 'POST':
        form = CadastroLivro(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/livro/home')
        else:
            return HttpResponse('DADOS INVÁLIDOS')
            

def excluir_livro(request, id):
    livro = Livro.objects.filter(id=id).delete()
    return redirect('/livro/home')


def cadastrar_categoria(request):
    form = CadastroCategoria(request.POST)
    nome = form.data['nome']
    descricao = form.data['descricao']    
    id_usuario = request.POST.get('usuario')
    if int(id_usuario) == int(request.session.get('usuario')):
        user = Usuario.objects.get(id = id_usuario)
        categoria = Categoria(nome=nome, descricao=descricao, usuario=user)
        categoria.save()
        return redirect('/livro/home?cadastro_categoria=1')
    else:
        return HttpResponse('ERRO')    

def cadastrar_emprestimo(request):
    if request.method == 'POST':
        nome_emprestado = request.POST.get('nome_emprestado')
        nome_emprestado_anonimo = request.POST.get('nome_emprestado_anonimo')
        livro_emprestado = request.POST.get('livro_emprestado')
        
        if nome_emprestado_anonimo:
            emprestimo = Emprestimos(nome_emprestado_anonimo = nome_emprestado_anonimo,
                                    livro_id = livro_emprestado)
        else:
            emprestimo = Emprestimos(nome_emprestado_id=nome_emprestado,
                                    livro_id = livro_emprestado)
        emprestimo.save()

        livro = Livro.objects.get(id = livro_emprestado)
        livro.emprestado = True
        livro.save()
        return redirect("/livro/home")
    
    
def devolver_livro(request):
    id = request.POST.get('id_livro_devolver')
    livro_devolver = Livro.objects.get(id = id)
    livro_devolver.emprestado = False
    livro_devolver.save()
    
    emprestimo_devolver = Emprestimos.objects.get(Q(livro = livro_devolver) & Q(data_devolucao = None) )
    emprestimo_devolver.data_devolucao = datetime.now() 
    emprestimo_devolver.save()

    return redirect('/livro/home')
      
    
def alterar_livro(request):
    livro_id = request.POST.get('livro_id')
    nome_livro = request.POST.get('nome_livro')
    autor = request.POST.get('autor')
    co_autor = request.POST.get('co_autor')
    categoria_id = request.POST.get('categoria_id')

    categoria = Categoria.objects.get(id = categoria_id)
    livro = Livro.objects.get(id = livro_id)
    if livro.usuario.id == request.session['usuario']:
        livro.nome = nome_livro
        livro.autor = autor
        livro.co_autor = co_autor
        livro.categoria = categoria
        livro.save()
        return redirect(f'/livro/ver_livro/{livro_id}')
    else:
        return redirect('/auth/sair')

def seus_emprestimos(request):
    usuario = Usuario.objects.get(id = request.session['usuario'])
    emprestimos = Emprestimos.objects.filter(nome_emprestado = usuario)
    


    return render(request, 'seus_emprestimos.html', {'usuario_logado': request.session['usuario'],
                                                    'emprestimos': emprestimos})

def processa_avaliacao(request):
    id_emprestimo = request.POST.get('id_emprestimo')
    opcoes = request.POST.get('opcoes')
    id_livro = request.POST.get('id_livro')
    #TODO: Verificar segurança
    #TODO: Não permitir avaliação de livro nao devolvido
    #TODO: Colocar as estrelas
    emprestimo = Emprestimos.objects.get(id = id_emprestimo)
    emprestimo.avaliacao = opcoes
    emprestimo.save()
    return redirect(f'/livro/ver_livro/{id_livro}')
    