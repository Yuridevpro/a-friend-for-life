# perfil/views.py

# Este arquivo contém as views para o app 'perfil'.
# Ele gerencia toda a lógica para exibir e interagir com os perfis dos usuários,
# incluindo a visualização do próprio perfil, a edição de dados, alteração de senha,
# remoção de conta, e a visualização do perfil público de outros protetores.

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import re
from django.contrib.auth import authenticate, logout
from django.shortcuts import get_object_or_404
from divulgar.models import Pet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import update_session_auth_hash


@login_required
def meu_perfil(request):
    """
    Exibe a página de perfil do usuário atualmente logado.
    Mostra suas informações, contadores de pets e a lista paginada
    dos animais que ele cadastrou.
    """
    user = request.user

    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        # Se o perfil ainda não existir, redireciona para a página de edição para forçar a criação.
        messages.error(request, 'Você precisa criar um perfil para acessar esta página.')
        return redirect('editar_perfil')

    # Contagem de pets divulgados pelo usuário.
    pets_divulgados = Pet.objects.filter(usuario=user).count()
    # Contagem de pets que foram marcados como adotados.
    pets_adotados = Pet.objects.filter(usuario=user, status='A').count() 

    # Busca todos os pets ativos cadastrados pelo usuário, ordenados pelos mais recentes.
    meus_pets = Pet.objects.filter(usuario=user, is_active=True).order_by('-id')

    # Configuração da paginação para a lista de pets.
    paginator = Paginator(meus_pets, 6) # Exibe 6 pets por página.
    page = request.GET.get('page') or 1 # Obtém o número da página da URL, padrão é 1.

    try:
        meus_pets = paginator.page(page)
    except PageNotAnInteger:
        # Se a página não for um inteiro, exibe a primeira página.
        meus_pets = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo (ex: 9999), exibe a última página.
        meus_pets = paginator.page(paginator.num_pages)

    # Lógica para criar uma lista de números de página amigável para a navegação.
    page_numbers = []
    current_page = meus_pets.number
    total_pages = paginator.num_pages

    if total_pages <= 7:
        page_numbers = list(range(1, total_pages + 1))
    else:
        # Lógica para exibir "..." quando há muitas páginas.
        if current_page <= 4:
            page_numbers = list(range(1, 6)) + ["...", total_pages]
        elif current_page >= total_pages - 3:
            page_numbers = [1, "..."] + list(range(total_pages - 4, total_pages + 1))
        else:
            page_numbers = [1, "..."] + list(range(current_page - 1, current_page + 2)) + ["...", total_pages]
    
    context = {
        'user': user,
        'pets_divulgados': pets_divulgados,
        'pets_adotados': pets_adotados,
        'meus_pets': meus_pets,
        'page_numbers': page_numbers,
    }
    return render(request, 'perfil/meu_perfil.html', context)
    

def perfil_protetor(request, user_id):
    """
    Exibe a página de perfil público de qualquer protetor.
    É similar a `meu_perfil`, mas para visualização de terceiros.
    Se o visitante for o próprio dono do perfil, ele é redirecionado
    para a sua própria página `meu_perfil`.
    """
    # Busca o usuário pelo ID fornecido na URL.
    user = get_object_or_404(User, pk=user_id)
    
    # Verifica se o visitante é o dono do perfil.
    is_owner = user == request.user
    if is_owner:
        # Se for o dono, redireciona para a visão privada do perfil.
        return redirect('meu_perfil')

    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        messages.error(request, 'Este usuário não possui um perfil.')
        return redirect('login')

    # Busca os pets ativos do protetor.
    pets = Pet.objects.filter(usuario=user, is_active=True) 
    pets_divulgados = pets.count()
    pets_adotados = Pet.objects.filter(usuario=user, status='A').count()

    # Lógica de paginação idêntica à de `meu_perfil`.
    paginator = Paginator(pets, 6) # Exibe 6 pets por página.
    page = request.GET.get('page') or 1

    try:
        pets = paginator.page(page)
    except PageNotAnInteger:
        pets = paginator.page(1)
    except EmptyPage:
        pets = paginator.page(paginator.num_pages)
    
    # Lógica de números de página idêntica à de `meu_perfil`.
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
        'user': user,
        'user_profile': user_profile,
        'pets': pets,
        'pets_adotados': pets_adotados,
        'profile_user': user,
        'pets_divulgados': pets_divulgados,
        'page_numbers': page_numbers,
    }
    return render(request, 'perfil/perfil_protetor.html', context)

    
@login_required
def ver_perfil(request, user_id):
    """
    View simples que busca um usuário por ID e renderiza uma página de perfil.
    (Nota: A lógica principal de visualização foi consolidada em 'perfil_protetor').
    """
    profile_user = get_object_or_404(User, id=user_id)
    return render(request, 'perfil/ver_perfil.html', {'profile_user': profile_user})


@login_required
def editar_perfil(request):
    """
    Processa a edição do perfil do usuário logado.
    - Se GET, exibe o formulário de edição pré-preenchido.
    - Se POST, valida os dados enviados, atualiza o modelo UserProfile
      e lida com o upload ou remoção da foto de perfil.
    """
    user = request.user
    
    # Busca o perfil do usuário ou cria um novo se não existir.
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        # Coleta os dados do formulário.
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        estado_id = request.POST.get('estado')
        estado_nome = request.POST.get('estado_nome')
        cidade = request.POST.get('cidade')
        foto_perfil = request.FILES.get('foto_perfil')
        remove_foto_perfil = request.POST.get('remove_foto_perfil') == 'true'

        # Validações dos campos.
        errors = []
        if not all([nome, sobrenome, telefone, estado_nome, cidade]):
            errors.append('Todos os campos com * são obrigatórios.')
        
        # Valida o formato do e-mail e telefone usando expressões regulares.
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            errors.append('Formato de e-mail inválido.')

        telefone_pattern = r'^\(?([0-9]{2})\)?[-. ]?([0-9]{4,5})[-. ]?([0-9]{4})$'
        if not re.match(telefone_pattern, telefone):
            errors.append('Formato de telefone inválido. Use (XX) XXXXX-XXXX.')

        # Verifica se o e-mail já está em uso por outra conta.
        if User.objects.filter(email=email).exclude(pk=user.pk).exists():
            errors.append('Este e-mail já está sendo usado por outro usuário.')

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('editar_perfil')

        # Atualiza os campos do objeto UserProfile.
        user_profile.nome = nome
        user_profile.sobrenome = sobrenome
        user_profile.telefone = telefone
        user_profile.estado_id = estado_id
        user_profile.estado_nome = estado_nome
        user_profile.cidade_nome = cidade
        user_profile.email = email
        
        # Lógica para atualizar a foto de perfil.
        if foto_perfil:
            user_profile.foto_perfil = foto_perfil
        elif remove_foto_perfil:
            if user_profile.foto_perfil:
                user_profile.foto_perfil.delete(save=False) # 'save=False' para salvar tudo de uma vez no final.
                
        user_profile.save()

        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('meu_perfil')
    
    else: # Requisição GET
        # Se o perfil for recém-criado e incompleto, exibe uma mensagem de aviso.
        if not all([user_profile.nome, user_profile.sobrenome, user_profile.telefone, user_profile.estado_nome, user_profile.cidade_nome]):
            messages.error(request, 'Você precisa preencher todos os campos do perfil antes de continuar.')

    return render(request, 'perfil/editar_perfil.html', {'user_profile': user_profile})


@login_required
@receiver(post_save, sender=UserProfile)
def update_user(sender, instance, created, **kwargs):
    """
    Este é um "signal receiver". Ele é executado automaticamente sempre que um
    objeto UserProfile é salvo. Sua função é manter os dados do modelo User
    padrão (como 'email' e 'username') sincronizados com o UserProfile.
    """
    user = instance.user
    
    if instance.email and (not user.email or user.email != instance.email):
        user.email = instance.email
    
    if not user.username or user.username != instance.email:
        user.username = instance.email
    
    user.save()


@login_required
def remover_foto_perfil(request):
    """
    Endpoint para remover a foto de perfil via uma requisição AJAX (POST).
    Retorna uma resposta JSON para o frontend.
    """
    if request.method == 'POST' and request.user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        user_profile.foto_perfil.delete(save=True) # Deleta o arquivo do S3 e salva o objeto.
        return JsonResponse({'message': 'Foto de perfil removida com sucesso.'})

    return JsonResponse({'error': 'Acesso não autorizado ou método inválido.'}, status=403)


@login_required
def alterar_senha(request):
    """
    Processa a alteração de senha para um usuário já logado.
    Valida a senha atual, a nova senha e a confirmação antes de salvar.
    """
    if request.method == 'POST':
        senha_atual = request.POST.get('senha_atual')
        senha_nova = request.POST.get('senha_nova')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not all([senha_atual, senha_nova, confirmar_senha]):
            messages.error(request, 'Preencha todos os campos.')
            return render(request, 'perfil/alterar_senha.html')

        # Verifica se a senha atual fornecida está correta.
        user = authenticate(request, username=request.user.username, password=senha_atual)
        if user is None:
            messages.error(request, 'Senha atual incorreta.')
            return render(request, 'perfil/alterar_senha.html')

        if senha_nova != confirmar_senha:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'perfil/alterar_senha.html')

        # Valida a força da nova senha.
        senha_pattern = r'^(?=.*[a-zA-Z])(?=.*[0-9]).{8,}$'
        if not re.match(senha_pattern, senha_nova):
            messages.error(request, 'A nova senha deve ter pelo menos 8 caracteres, com letras e números.')
            return render(request, 'perfil/alterar_senha.html')

        try:
            # Salva a nova senha (o Django cuida do hash).
            user.set_password(senha_nova)
            user.save()
            # Atualiza a sessão para que o usuário não seja deslogado após a troca de senha.
            update_session_auth_hash(request, user)
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('meu_perfil')
        except Exception as e:
            messages.error(request, f'Erro ao alterar senha: {str(e)}')
            return render(request, 'perfil/alterar_senha.html')
    else:
        return render(request, 'perfil/alterar_senha.html')

@login_required
def remover_pet(request, id):
    """
    Desativa o anúncio de um pet.
    Verifica se o usuário logado é o dono do pet antes de realizar a ação.
    A remoção é "lógica" (soft delete), apenas marcando o pet como inativo.
    """
    pet = get_object_or_404(Pet, id=id)
    # Verificação de propriedade.
    if not pet.usuario == request.user:
        messages.error(request, 'Esse pet não é seu!')
        return redirect('/divulgar/seus_pets')

    pet.is_active = False
    pet.save()
    messages.success(request, 'Pet removido com sucesso.')
    return redirect('meu_perfil') 

@login_required
@csrf_exempt
def remover_conta(request):
    """
    Remove permanentemente a conta do usuário e todos os seus dados associados.
    Esta é uma ação destrutiva (hard delete).
    """
    if request.method == 'POST':
        user = request.user
        try:
            user.delete() # Deleta o usuário e, por cascata, seu perfil e outros dados.
            logout(request) # Encerra a sessão.
            messages.success(request, 'Conta removida com sucesso!')
            return redirect('login') 
        except Exception as e:
            messages.error(request, f'Erro ao remover conta: {str(e)}')
            return JsonResponse({'error': str(e)}, status=400) 
    else:
        return JsonResponse({'error': 'Método inválido.'}, status=405)

@login_required
def sair(request):
    """
    View de logout, redirecionada do `usuarios/views.py`.
    """
    logout(request)
    return redirect('/auth/login')