from django.contrib import admin
from .models import Usuario

# n~so permite que o o administardor modifique os dados dos usuários
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    readonly_fields = ("nome", "email", "senha")
