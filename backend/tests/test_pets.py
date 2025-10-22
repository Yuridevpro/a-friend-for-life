# backend/tests/test_pets.py (VERSÃO SIMPLIFICADA E CORRETA)

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from divulgar.models import Pet
from perfil.models import UserProfile

class DivulgarEPerfilTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.password = 'password123'
        
        self.dono = User.objects.create_user('dono@example.com', 'dono@example.com', self.password)
        UserProfile.objects.create(
            user=self.dono, nome="Dono", sobrenome="Teste", telefone="11999999999",
            email="dono@example.com", estado_nome="SP", cidade_nome="Sao Paulo"
        )
        
        self.invasor = User.objects.create_user('invasor@example.com', 'invasor@example.com', self.password)
        UserProfile.objects.create(
            user=self.invasor, nome="Invasor", sobrenome="User", telefone="11888888888",
            email="invasor@example.com", estado_nome="RJ", cidade_nome="Rio de Janeiro"
        )

        self.pet = Pet.objects.create(
            usuario=self.dono, nome_pet="TestDog", especie="Cachorro",
            sexo="Macho", tamanho="Médio"
        )

    def test_dono_pode_acessar_pagina_edicao(self):
        self.client.login(username='dono@example.com', password=self.password)
        response = self.client.get(reverse('editar_pet', kwargs={'id': self.pet.id}))
        self.assertEqual(response.status_code, 200)
    
    def test_invasor_nao_pode_acessar_pagina_edicao(self):
        self.client.login(username='invasor@example.com', password=self.password)
        response = self.client.get(reverse('editar_pet', kwargs={'id': self.pet.id}))
        self.assertRedirects(response, reverse('meu_perfil'))

    def test_middleware_forca_redirecionamento(self):
        """
        Testa se o middleware redireciona um usuário com perfil incompleto.
        """
        user_incompleto = User.objects.create_user('incompleto@test.com', 'incompleto@test.com', self.password)
        UserProfile.objects.create(user=user_incompleto, nome="Incompleto")

        self.client.login(username='incompleto@test.com', password=self.password)
        response = self.client.get(reverse('listar_pets'))
        # Apenas verifica se o middleware causou um redirecionamento.
        self.assertEqual(response.status_code, 302)