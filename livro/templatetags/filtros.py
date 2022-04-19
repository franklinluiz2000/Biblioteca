from django import template

register = template.Library()

@register.filter
def mostra_duracao(dataDevolucao, dataEmprestimo):
    return (dataDevolucao - dataEmprestimo).days