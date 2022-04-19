from django.contrib import admin
from .models import Livro, Categoria, Emprestimos

admin.site.register(Categoria)
admin.site.register(Livro)
admin.site.register(Emprestimos)


