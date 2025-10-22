# perfil/middleware.py

# Este arquivo define um Middleware personalizado do Django.
# Um Middleware intercepta todas as requisições e respostas do site.
# Este, em específico ('ProfileCompleteMiddleware'), verifica se o usuário
# logado já preencheu todas as informações obrigatórias do seu perfil.
# Se o perfil estiver incompleto, ele redireciona o usuário para a página de
# edição de perfil, forçando-o a completar o cadastro antes de poder usar
# as outras funcionalidades do site.

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib.auth import logout
from django.urls import reverse

class ProfileCompleteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # O middleware é executado para cada requisição.
        
        # Verifica se o usuário está autenticado e não é um superusuário.
        if request.user.is_authenticated and not request.user.is_superuser:
            # Obtém o perfil do usuário, ou cria um se não existir.
            profile = UserProfile.objects.get_or_create(user=request.user)[0]
            
            # Verifica se algum dos campos obrigatórios do perfil está vazio.
            if not profile.nome or not profile.sobrenome or not profile.telefone or not profile.estado_nome or not profile.cidade_nome:
                # Permite o acesso a rotas essenciais (editar perfil, login, logout)
                # mesmo com o perfil incompleto, para evitar um loop infinito de redirecionamento.
                allowed_paths = [reverse('editar_perfil'), '/auth/logout/', '/auth/login/']
                if request.path not in allowed_paths:
                    # Se o perfil está incompleto e o usuário tenta acessar outra página,
                    # ele é redirecionado para a página de edição de perfil.
                    return redirect(reverse('editar_perfil'))

        # Se o perfil estiver completo ou o usuário não estiver logado,
        # a requisição continua seu fluxo normal.
        return self.get_response(request)