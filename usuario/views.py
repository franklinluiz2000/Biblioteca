from django.shortcuts import render
from django.http import HttpResponse
from  .models import Usuario
from django.shortcuts import redirect
from hashlib import sha256


def login(request):
    if request.session.get('usuario'):
        return redirect("/livro/home/")
    
    # o GET é o tipo do método e o get é o que pega o resultado
    status = request.GET.get("status")
    return render(request, "login.html", {"status": status})
    
def cadastro(request):
    if request.session.get('usuario'):
        return redirect("/livro/home/")
    
    # o GET é o tipo do método e o get é o que pega o resultado
    status = request.GET.get("status")
    return render(request, "cadastro.html", {"status": status})

def valida_cadastro(request):
    nome = request.POST.get('nome')
    senha = request.POST.get('senha')
    email = request.POST.get('email')

    # Pesquisa se os dados existe no banco de dados
    usuario = Usuario.objects.filter(email=email)

    # Verifica se o nome ou o email está em branco
    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        return redirect("/auth/cadastro/?status=1")

    # Verificação se a senha é maior menor que 8
    if len(senha) < 8:
        return redirect("/auth/cadastro/?status=2")

    # verifica se já existe o usuaário já cadastrado
    if len(usuario) > 0:
        return redirect("/auth/cadastro/?status=3")

    try:
        # tranforma a senha em um hexadecimal depois de convertida para binário
        senha = sha256(senha.encode()).hexdigest()

        usuario = Usuario(nome = nome, senha = senha, email=email)
        usuario.save()
        return redirect("/auth/cadastro/?status=0")

    except:
        return redirect("/auth/cadastro/?status=4")
    

def valida_login(request):
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    # transforma a senha em binário e depois em hexadecimal
    senha = sha256(senha.encode()).hexdigest()

    # Pesquisa se os dados existe no banco de dados
    usuario = Usuario.objects.filter(email=email).filter(senha=senha)

    # testa se usuário existir ele direciona para a página de livro
    if len(usuario) == 0:
        return redirect("/auth/login/?status=1")
    elif len(usuario) > 0:
        request.session['usuario'] = usuario[0].id
        return redirect("/livro/home/")

    return HttpResponse(f"{email} {senha}")


def sair(request):
    # sai da tela de livros, lipando o registro usuário
    request.session.flush()
    return redirect("/auth/login/")