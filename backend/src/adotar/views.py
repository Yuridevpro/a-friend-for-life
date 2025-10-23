# adotar/views.py

# Este arquivo contém as views para o app 'adotar'. A principal funcionalidade
# é a listagem de pets disponíveis para adoção, com um sistema de filtros
# que permite aos usuários refinar a busca por localização (estado/cidade),
# tamanho e espécie do animal. A view também implementa a paginação para
# exibir os resultados de forma organizada.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import transaction
from django.core.mail import send_mail
from django.utils.timezone import now
from django.http import JsonResponse
from divulgar.models import Pet
from adote.settings import constants
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests

@login_required
def listar_pets(request):
    """
    Exibe a lista de pets disponíveis para adoção.
    - Filtra apenas os pets que estão ativos ('is_active=True') e com status
      'Para adoção' ('P').
    - Aplica os filtros de busca enviados via GET (estado, cidade, tamanho, especie).
    - Implementa a paginação para dividir os resultados em várias páginas.
    """
    # Busca inicial de pets no banco, ordenando pelos mais recentes.
    pets_list = Pet.objects.filter(status__in=["P"], is_active=True).order_by('-created_at')

    # Obtém os valores de filtro da URL (query parameters).
    estado_id = request.GET.get('estado')
    cidade_nome = request.GET.get('cidade')
    tamanho = request.GET.get('tamanho')
    especie = request.GET.get('especie')

    # Aplica os filtros na consulta ao banco de dados, se eles existirem.
    # A filtragem de localização é feita através do perfil do usuário que cadastrou o pet.
    if estado_id:
        pets_list = pets_list.filter(usuario__userprofile__estado_id=estado_id)
    if cidade_nome:
        pets_list = pets_list.filter(usuario__userprofile__cidade_nome=cidade_nome)
    if tamanho:
        pets_list = pets_list.filter(tamanho=tamanho)
    if especie:
        pets_list = pets_list.filter(especie=especie)

    # Passa as opções de escolha para o template popular os seletores do formulário.
    choices_especie = Pet.choices_especie
    choices_tamanho = Pet.choices_tamanho

    # Configuração da paginação.
    paginator = Paginator(pets_list, 12)  # Exibe 12 pets por página.
    page = request.GET.get('page') or 1  # Obtém o número da página, o padrão é 1.

    try:
        pets = paginator.page(page)
    except PageNotAnInteger:
        # Se 'page' não for um número, exibe a primeira página.
        pets = paginator.page(1)
    except EmptyPage:
        # Se 'page' estiver fora do intervalo, exibe a última página.
        pets = paginator.page(paginator.num_pages)

    # Lógica para criar a navegação da paginação de forma amigável (com "...").
    page_numbers = []
    current_page = pets.number
    total_pages = paginator.num_pages

    if total_pages <= 7:
        page_numbers = list(range(1, total_pages + 1))
    else:
        if current_page <= 4:
            page_numbers = list(range(1, 6)) + ["...", total_pages]
        elif current_page >= total_pages - 3:
            page_numbers = [1, "..."] + list(range(total_pages - 4, total_pages + 1))
        else:
            page_numbers = [1, "..."] + list(range(current_page - 1, current_page + 2)) + ["...", total_pages]
    
    context = {
        'pets': pets,
        'cidade_nome': cidade_nome,
        'estado_id': estado_id,
        'tamanho': tamanho,
        'especie': especie,
        'choices_especie': choices_especie,
        'choices_tamanho': choices_tamanho,
        'page_numbers': page_numbers,
    }
    return render(request, 'adotar/listar_pets.html', context)