# pagina_inicio/views.py


# Este arquivo contém as views para o app 'pagina_inicio'.
# A view 'home' é a principal do site, exibindo uma lista de pets recentes,
# filtros de busca e depoimentos. As outras views gerenciam o ciclo de vida
# dos depoimentos (criar, editar, deletar) e fornecem um endpoint para
# carregar mais depoimentos dinamicamente via AJAX.

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from divulgar.models import Pet
from perfil.models import UserProfile
from .models import Depoimento
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

def home(request):
    """
    Renderiza a página inicial do site.
    - Exibe uma lista paginada dos pets mais recentes para adoção.
    - Mostra os filtros de busca.
    - Exibe os depoimentos mais recentes.
    """
    pets_list = Pet.objects.filter(status__in=["P"], is_active=True).order_by('-created_at')
    
    # Aplica filtros de busca se presentes na URL.
    estado_id = request.GET.get('estado')
    cidade_nome = request.GET.get('cidade')
    tamanho = request.GET.get('tamanho')
    especie = request.GET.get('especie')

    if estado_id:
        pets_list = pets_list.filter(usuario__userprofile__estado_id=estado_id)
    if cidade_nome:
        pets_list = pets_list.filter(usuario__userprofile__cidade_nome=cidade_nome)
    if tamanho:
        pets_list = pets_list.filter(tamanho=tamanho)
    if especie:
        pets_list = pets_list.filter(especie=especie)

    choices_especie = Pet.choices_especie
    choices_tamanho = Pet.choices_tamanho
    
    # Paginação para a lista de pets.
    paginator = Paginator(pets_list, 6) # 6 pets por página.
    page = request.GET.get('page') or 1

    try:
        pets = paginator.page(page)
    except PageNotAnInteger:
        pets = paginator.page(1)
    except EmptyPage:
        pets = paginator.page(paginator.num_pages)

    # Lógica de navegação da paginação.
    page_numbers = []
    current_page = pets.number
    total_pages = paginator.num_pages

    if total_pages <= 7:
        page_numbers = list(range(1, total_pages + 1))
    else:
        # Adiciona "..." para paginações longas.
        if current_page <= 4:
            page_numbers = list(range(1, 6)) + ["...", total_pages]
        elif current_page >= total_pages - 3:
            page_numbers = [1, "..."] + list(range(total_pages - 4, total_pages + 1))
        else:
            page_numbers = [1, "..."] + list(range(current_page - 1, current_page + 2)) + ["...", total_pages]

    # Paginação para os depoimentos.
    depoimentos_list = Depoimento.objects.order_by('-data_criacao')
    depoimentos_paginator = Paginator(depoimentos_list, 3) # 3 depoimentos por vez.
    depoimentos = depoimentos_paginator.page(1)

    # Verifica se há mais páginas de depoimentos para mostrar o botão "Mais...".
    mais_depoimentos = depoimentos_paginator.num_pages > 1

    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            # Garante que um usuário logado tenha um perfil para evitar erros.
            return redirect('editar_perfil') 

    context = {
        'pets': pets, 'page_numbers': page_numbers,
        'choices_especie': choices_especie, 'choices_tamanho': choices_tamanho,
        'estado_id': estado_id, 'cidade_nome': cidade_nome,
        'tamanho': tamanho, 'especie': especie,
        'depoimentos': depoimentos, 'mais_depoimentos': mais_depoimentos,
        'user_profile': user_profile,
    }
    return render(request, 'pagina_inicio/home.html', context)

@login_required
def criar_depoimento(request):
    """
    Gerencia a criação e edição de depoimentos.
    - Se um usuário já tem um depoimento, esta view permite que ele o edite.
    - Se não, permite a criação de um novo.
    A lógica de "criar ou atualizar" (upsert) é implementada para simplificar
    a experiência do usuário, tratando o depoimento como um recurso único por usuário.
    """
    if request.method == 'POST':
        mensagem = request.POST.get('mensagem')
        # Obtém dados do perfil do usuário para associar ao depoimento.
        nome = request.user.userprofile.nome
        sobrenome = request.user.userprofile.sobrenome
        email = request.user.userprofile.email

        try:
            # Tenta encontrar um depoimento existente pelo e-mail do usuário.
            depoimento = Depoimento.objects.get(email=email)
            # Se encontrar, atualiza a mensagem.
            depoimento.mensagem = mensagem
            depoimento.save()
            messages.success(request, 'Depoimento atualizado com sucesso!')
        except Depoimento.DoesNotExist:
            # Se não encontrar, cria um novo depoimento.
            Depoimento.objects.create(nome=nome, sobrenome=sobrenome, email=email, mensagem=mensagem, usuario=request.user)
            messages.success(request, 'Depoimento enviado com sucesso!')

        return redirect('depoimento')

    # Se a requisição for GET, busca o depoimento existente para preencher o formulário.
    try:
        depoimento = Depoimento.objects.get(email=request.user.userprofile.email)
    except Depoimento.DoesNotExist:
        depoimento = None

    context = {
        'depoimento': depoimento,
        'nome': request.user.userprofile.nome,
        'sobrenome': request.user.userprofile.sobrenome
    }
    return render(request, 'pagina_inicio/depoimento.html', context)

@login_required
def editar_depoimento(request, pk):
    """
    View específica para editar um depoimento. (Nota: a lógica principal foi
    consolidada em 'criar_depoimento' para uma melhor experiência do usuário).
    """
    depoimento = get_object_or_404(Depoimento, pk=pk)

    if request.method == 'POST':
        mensagem = request.POST.get('mensagem')
        depoimento.mensagem = mensagem
        depoimento.save()
        messages.success(request, 'Depoimento atualizado com sucesso!')
        return redirect('depoimento')

    context = {
        'depoimento': depoimento,
        'nome': request.user.userprofile.nome,
        'sobrenome': request.user.userprofile.sobrenome
    }
    return render(request, 'pagina_inicio/depoimento.html', context)

@login_required
def deletar_depoimento(request, pk):
    """
    Processa a exclusão de um depoimento.
    """
    depoimento = get_object_or_404(Depoimento, pk=pk)
    if request.method == 'POST':
        depoimento.delete()
        messages.success(request, 'Depoimento deletado com sucesso!')
        return redirect('depoimento')
    return render(request, 'pagina_inicio/depoimento.html', {'depoimento': depoimento})

@login_required
def mais_depoimentos(request):
    """
    Endpoint de API para carregar mais depoimentos via AJAX.
    Recebe o número da página atual e retorna a próxima página de depoimentos
    em formato JSON.
    """
    depoimentos_list = Depoimento.objects.order_by('-data_criacao')
    depoimentos_paginator = Paginator(depoimentos_list, 3)

    pagina_atual = int(request.GET.get('pagina_atual', 1))
    try:
        # Tenta carregar a próxima página.
        depoimentos = depoimentos_paginator.page(pagina_atual + 1)
    except EmptyPage:
        # Se não houver mais páginas, retorna uma lista vazia.
        return JsonResponse({'depoimentos': []})

    if depoimentos:
        # Formata os dados dos depoimentos para a resposta JSON.
        depoimentos_json = [
            {
                'mensagem': depoimento.mensagem,
                'nome': depoimento.nome,
                'sobrenome': depoimento.sobrenome,
            }
            for depoimento in depoimentos
        ]
        return JsonResponse({'depoimentos': depoimentos_json})
    else:
        return JsonResponse({'depoimentos': []})