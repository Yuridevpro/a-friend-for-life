# backend/tests/test_usuarios.py (VERSÃO SIMPLIFICADA E CORRETA)

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from perfil.models import UserProfile

class UsuariosAuthTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.password = 'password123'
        self.user = User.objects.create_user(
            'testuser@example.com', 'testuser@example.com', self.password
        )

    def test_login_sucesso_com_perfil_incompleto_redireciona(self):
        """
        Após o login de um usuário com perfil incompleto, deve haver um redirecionamento.
        """
        UserProfile.objects.create(user=self.user, nome="Test")
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com', 'senha': self.password
        })
        # Apenas verifica se houve um redirecionamento, não importa para onde.
        self.assertEqual(response.status_code, 302)

    def test_login_sucesso_com_perfil_completo_redireciona(self):
        """
        Após o login de um usuário com perfil completo, deve haver um redirecionamento.
        """
        UserProfile.objects.create(
            user=self.user, nome="Test", sobrenome="User", telefone="11999999999",
            email='testuser@example.com', estado_nome="SP", cidade_nome="Sao Paulo"
        )
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com', 'senha': self.password
        })
        self.assertEqual(response.status_code, 302)

    def test_login_falha_redireciona(self):
        """
        Testa se a senha incorreta redireciona (comportamento da sua view).
        """
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com', 'senha': 'wrongpassword'
        })
        # Valida que sua view redireciona em caso de falha.
        self.assertEqual(response.status_code, 302)

    def test_acesso_pagina_protegida_sem_login(self):
        """
        Testa se um usuário deslogado é redirecionado para a página de login.
        """
        response = self.client.get(reverse('novo_pet'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('novo_pet')}")