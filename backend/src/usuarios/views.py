# usuarios/views.py

# Este arquivo contém a lógica de controle (views) para o app 'usuarios'.
# Cada função aqui representa uma "página" ou uma ação que o usuário pode realizar,
# como se cadastrar, fazer login, confirmar e-mail, solicitar a redefinição de senha,
# criar uma nova senha e fazer logout. As views processam as requisições do usuário,
# interagem com os modelos e renderizam os templates HTML como resposta.

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from perfil.models import UserProfile
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import re
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from .models import Ativacao, ResetSenha
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction

# Importa a função de envio de e-mail assíncrono do arquivo utils.py
from .utils import enviar_email_com_template


@transaction.atomic
def cadastro(request):
    """
    Processa o cadastro de novos usuários.
    - Se a requisição for GET, exibe o formulário de cadastro.
    - Se a requisição for POST, valida os dados, cria um novo usuário (inativo)
      e seu perfil, gera um token de ativação e envia um e-mail de confirmação.
    - O decorator @transaction.atomic garante que a criação do usuário e do perfil
      sejam uma operação única: ou ambos são criados com sucesso, ou nada é salvo no banco.
    """
    # Redireciona usuários já autenticados para a página principal.
    if request.user.is_authenticated:
        return redirect('/divulgar/novo_pet')

    if request.method == "POST":
        # Coleta de dados do formulário
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        telefone = request.POST.get('telefone')
        estado_id = request.POST.get('estado_id')
        estado_nome = request.POST.get('estado_nome')
        cidade_nome = request.POST.get('cidade_nome')

        # Validação de campos obrigatórios
        if not all([nome, sobrenome, email, senha, confirmar_senha, telefone, estado_id, cidade_nome]):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos obrigatórios.')
            return render(request, 'usuarios/cadastro.html', {'nome': nome, 'sobrenome': sobrenome, 'email': email, 'telefone': telefone, 'estado_id': estado_id, 'cidade_nome': cidade_nome})

        # Validação de senhas
        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem.')
            return render(request, 'usuarios/cadastro.html', {'nome': nome, 'sobrenome': sobrenome, 'email': email, 'telefone': telefone, 'estado_id': estado_id, 'cidade_nome': cidade_nome})

        # Valida o formato do e-mail usando expressão regular (Regex)
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            messages.add_message(request, constants.ERROR, 'O formato do e-mail é inválido.')
            return render(request, 'usuarios/cadastro.html', {'nome': nome, 'sobrenome': sobrenome, 'email': email, 'telefone': telefone, 'estado_id': estado_id, 'cidade_nome': cidade_nome})

        # Valida a força da senha (mínimo 8 caracteres, com letras e números)
        senha_pattern = r'^(?=.*[a-zA-Z])(?=.*[0-9]).{8,}$'
        if not re.match(senha_pattern, senha):
            messages.add_message(request, constants.ERROR, 'A senha deve conter pelo menos 8 caracteres, incluindo letras e números.')
            return render(request, 'usuarios/cadastro.html', {'nome': nome, 'sobrenome': sobrenome, 'email': email, 'telefone': telefone, 'estado_id': estado_id, 'cidade_nome': cidade_nome})

        try:
            # Verifica se o e-mail já existe
            user_existente = User.objects.filter(email=email).first()
            if user_existente:
                if not user_existente.is_active:
                    # Se o usuário existe mas está inativo (cadastro não confirmado),
                    # apaga o registro antigo para permitir um novo cadastro limpo.
                    user_existente.delete()
                else:
                    # Se o usuário já existe e está ativo, informa o erro.
                    messages.error(request, 'Este e-mail já está em uso por uma conta ativa.')
                    return redirect('cadastro')

            # Cria o usuário (inativo) e o perfil associado
            user = User.objects.create_user(username=email, email=email, password=senha, is_active=False)
            UserProfile.objects.create(
                user=user, telefone=telefone, estado_nome=estado_nome, estado_id=estado_id,
                cidade_nome=cidade_nome, nome=nome, sobrenome=sobrenome, email=email
            )

            # Gera um token de ativação único e aleatório
            token = get_random_string(length=32)
            Ativacao.objects.create(
                user=user,
                confirmation_token=token,
                confirmation_token_expiration=timezone.now() + timedelta(days=1) # Token expira em 1 dia
            )

            # Prepara o contexto de dados para o template do e-mail
            context = {
                'user': user,
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), # Codifica o ID do usuário
                'token': token,
            }
            # Envia o e-mail de confirmação de forma assíncrona
            enviar_email_com_template(
                request,
                subject='Confirmação de Cadastro - A Friend for Life',
                template_name='usuarios/email_confirmacao.html',
                context=context,
                recipient_list=[user.email]
            )

            messages.success(request, 'Cadastro realizado com sucesso! Um e-mail de confirmação foi enviado. Por favor, verifique sua caixa de entrada e também a pasta de SPAM.')
            return redirect('login')

        except Exception as e:
            # Em caso de qualquer erro inesperado, exibe uma mensagem genérica
            messages.error(request, f'Ocorreu um erro inesperado durante o cadastro. Nenhuma conta foi criada.')
            # Loga o erro no console para depuração
            print(f"Erro de cadastro: {e}")
            return redirect('cadastro')

    # Se a requisição for GET, apenas renderiza a página de cadastro
    return render(request, 'usuarios/cadastro.html')


def confirmar_email(request, uidb64, token):
    """
    Valida o link de confirmação de e-mail clicado pelo usuário.
    Se o ID do usuário e o token forem válidos e não tiverem expirado,
    ativa a conta do usuário e o redireciona para a página de login.
    """
    try:
        # Decodifica o ID do usuário e busca os objetos no banco
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        ativacao = Ativacao.objects.get(user=user, confirmation_token=token)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, Ativacao.DoesNotExist):
        user = None
        ativacao = None

    # Verifica se o usuário e o token são válidos e se o token não expirou
    if user is not None and ativacao is not None and ativacao.confirmation_token_expiration > timezone.now():
        # Ativa o usuário e remove o registro de ativação
        user.is_active = True
        user.save()
        ativacao.delete()
        messages.add_message(request, constants.SUCCESS, 'Email confirmado com sucesso! Você já pode fazer o login.')
        return redirect('login')
    else:
        # Caso o link seja inválido ou expirado
        messages.add_message(request, constants.ERROR, 'Link de confirmação inválido ou expirado. Por favor, tente se cadastrar novamente.')
        return redirect('cadastro')


def logar(request):
    """
    Processa o login de um usuário.
    - Se GET, exibe a página de login.
    - Se POST, valida as credenciais. Se corretas, inicia a sessão do usuário.
      Também verifica se a conta do usuário já foi ativada.
    """
    if request.user.is_authenticated:
        return redirect('/divulgar/novo_pet')
        
    if request.method == "POST":
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if not email or not senha:
            messages.error(request, 'E-mail e senha são obrigatórios.')
            return redirect('login')

        try:
            # Primeiro, verifica se o usuário existe e se a conta está ativa
            user_obj = User.objects.get(email=email)
            if not user_obj.is_active:
                messages.warning(request, 'Sua conta ainda não foi ativada. Verifique seu e-mail de confirmação.')
                return redirect('login')
        except User.DoesNotExist:
            # Se o usuário não existe, a função 'authenticate' abaixo cuidará da mensagem de erro
            pass

        # Tenta autenticar o usuário com e-mail (username) and senha
        user = authenticate(request, username=email, password=senha)
        if user is not None:
            # Se a autenticação for bem-sucedida, inicia a sessão
            login(request, user)
            messages.success(request, f'Bem-vindo(a) de volta!')
            return redirect('/divulgar/novo_pet')
        else:
            # Se as credenciais estiverem incorretas
            messages.error(request, 'E-mail ou senha inválidos.')
            return redirect('login')

    return render(request, 'usuarios/login.html')


def esqueceu_senha(request):
    """
    Inicia o processo de redefinição de senha.
    - Se GET, exibe o formulário para inserir o e-mail.
    - Se POST, verifica se o e-mail existe, gera um token de redefinição
      e envia um e-mail com o link para criar uma nova senha.
    """
    if request.method == "POST":
        email_form = request.POST.get('email')
        if not email_form:
            messages.add_message(request, constants.ERROR, 'Por favor, informe um e-mail válido.')
            return render(request, 'usuarios/esqueceu_senha.html')
        
        try:
            user = User.objects.get(email=email_form)
            
            # Garante que tokens antigos para o mesmo usuário sejam invalidados
            ResetSenha.objects.filter(user=user).delete()

            # Cria um novo token de redefinição seguro
            token = default_token_generator.make_token(user)
            ResetSenha.objects.create(user=user, reset_token=token)

            # Prepara o contexto e envia o e-mail
            context = {
                'user': user,
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            }
            enviar_email_com_template(
                request,
                subject='Redefinição de Senha - A Friend for Life',
                template_name='usuarios/email_reset_senha.html',
                context=context,
                recipient_list=[user.email]
            )
            
            messages.success(request, 'Um e-mail com instruções para redefinir sua senha foi enviado. Verifique sua caixa de entrada e também a pasta de SPAM.')
            return redirect('login')

        except User.DoesNotExist:
            # Por segurança, não informa que o e-mail não existe.
            # Exibe uma mensagem genérica para evitar que atacantes descubram e-mails cadastrados.
            messages.success(request, 'Se houver uma conta associada a este e-mail, um link de redefinição de senha foi enviado.')
            return redirect('login')
        except Exception as e:
            messages.error(request, 'Ocorreu um erro ao processar sua solicitação. Tente novamente mais tarde.')
            print(f"Erro em esqueceu_senha: {e}")
            return redirect('esqueceu_senha')
    
    return render(request, 'usuarios/esqueceu_senha.html')


def criar_senha(request, uidb64, token):
    """
    Permite ao usuário definir uma nova senha a partir de um link de redefinição.
    - Se GET, exibe o formulário para digitar a nova senha.
    - Se POST, valida a nova senha, a salva no banco e invalida o token.
    """
    try:
        # Decodifica o ID do usuário e busca os objetos no banco
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = User.objects.get(pk=uid)
        reset_senha_obj = ResetSenha.objects.get(user=user)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ResetSenha.DoesNotExist):
        user = None
        reset_senha_obj = None

    # Verifica se o link é válido (usuário existe, token corresponde e não expirou)
    if user is not None and reset_senha_obj is not None and reset_senha_obj.reset_token == token and reset_senha_obj.is_token_valid():
        if request.method == 'POST':
            senha_nova = request.POST.get('senha_nova')
            confirmar_senha = request.POST.get('confirmar_senha')

            # Validações da nova senha
            if not senha_nova or not confirmar_senha:
                messages.add_message(request, constants.ERROR, 'Ambos os campos de senha são obrigatórios.')
                return render(request, 'usuarios/criar_senha.html', {'uidb64': uidb64, 'token': token})

            if senha_nova != confirmar_senha:
                messages.add_message(request, constants.ERROR, 'As senhas não coincidem.')
                return render(request, 'usuarios/criar_senha.html', {'uidb64': uidb64, 'token': token})
            
            senha_pattern = r'^(?=.*[a-zA-Z])(?=.*[0-9]).{8,}$'
            if not re.match(senha_pattern, senha_nova):
                messages.add_message(request, constants.ERROR, 'A nova senha deve conter pelo menos 8 caracteres, incluindo letras e números.')
                return render(request, 'usuarios/criar_senha.html', {'uidb64': uidb64, 'token': token})

            # Define a nova senha e a salva de forma segura (com hash)
            user.set_password(senha_nova)
            user.save()
            # Remove o token de redefinição para que não possa ser usado novamente
            reset_senha_obj.delete()
            
            messages.success(request, 'Sua senha foi alterada com sucesso! Faça login com sua nova senha.')
            return redirect('login')
        else:
            # Se GET, apenas exibe a página para criar a nova senha
            return render(request, 'usuarios/criar_senha.html', {'uidb64': uidb64, 'token': token})
    else:
        # Se o link for inválido ou expirado
        messages.error(request, 'O link de redefinição de senha é inválido ou já expirou. Por favor, solicite um novo.')
        return redirect('esqueceu_senha')

@login_required
def sair(request):
    """
    Encerra a sessão do usuário logado (logout).
    O decorator @login_required garante que apenas usuários autenticados
    possam acessar esta funcionalidade.
    """
    logout(request)
    messages.info(request, 'Você saiu da sua conta com sucesso.')
    return redirect('login')

# Adicione esta função no final do arquivo backend/src/usuarios/views.py

def reenviar_ativacao(request):
    """
    Permite que um usuário com conta inativa solicite um novo e-mail de ativação.
    - Se GET, exibe o formulário para inserir o e-mail.
    - Se POST, verifica se existe um usuário inativo com o e-mail fornecido,
      deleta o token de ativação antigo, cria um novo e o reenvia.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Verifica se a conta já está ativa
            if user.is_active:
                messages.info(request, 'Esta conta já está ativa. Você pode fazer o login.')
                return redirect('login')
            
            # Deleta tokens de ativação antigos para este usuário
            Ativacao.objects.filter(user=user).delete()
            
            # Cria um novo token de ativação
            token = get_random_string(length=32)
            Ativacao.objects.create(
                user=user,
                confirmation_token=token,
                confirmation_token_expiration=timezone.now() + timedelta(days=1)
            )
            
            # Prepara o contexto para o e-mail
            context = {
                'user': user,
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            }

            # Envia o novo e-mail
            enviar_email_com_template(
                request,
                subject='Novo Link de Ativação - A Friend for Life',
                template_name='usuarios/email_confirmacao.html', # Reutiliza o mesmo template
                context=context,
                recipient_list=[user.email]
            )
            
            messages.success(request, 'Um novo e-mail de ativação foi enviado. Verifique sua caixa de entrada e também a pasta de SPAM.')
            return redirect('login')
            
        except User.DoesNotExist:
            messages.error(request, 'Nenhum usuário inativo encontrado com este e-mail.')
            return redirect('reenviar_ativacao')

    return render(request, 'usuarios/reenviar_ativacao.html')