# sobre_nos/views.py

# Este arquivo contém as views para o app 'sobre_nos'.
# Cada função aqui é muito simples: ela apenas recebe uma requisição
# e renderiza o template HTML correspondente para exibir as informações
# institucionais da plataforma de forma estática.

from django.shortcuts import render

def quem_somos(request):
    """Renderiza a página 'Quem Somos'."""
    return render(request, 'sobre_nos/quem_somos.html')

def politica_privacidade(request):
    """Renderiza a página 'Política de Privacidade'."""
    return render(request, 'sobre_nos/politica_privacidade.html')

def termos_servico(request):
    """Renderiza a página 'Termos de Serviço'."""
    return render(request, 'sobre_nos/termos_servico.html')
