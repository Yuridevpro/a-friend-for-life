# usuarios/models.py

# Este arquivo define os modelos de dados para o app 'usuarios'.
# Ele contém as classes que representam as tabelas no banco de dados
# relacionadas à funcionalidade de usuários, como a ativação de contas
# e a redefinição de senhas.

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Ativacao(models.Model):
    """
    Armazena o token de ativação temporário para um novo usuário.
    Quando um usuário se cadastra, um registro neste modelo é criado,
    associando o usuário a um token único com data de validade.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    confirmation_token = models.CharField(max_length=32, blank=True)
    confirmation_token_expiration = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username



class ResetSenha(models.Model):
    """
    Armazena o token temporário para redefinição de senha.
    Este modelo garante uma associação de um para um (OneToOneField) com o usuário,
    significando que um usuário só pode ter um pedido de redefinição de senha ativo por vez.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reset_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_token_valid(self):
        """
        Verifica se o token ainda está dentro do período de validade (24 horas).
        Retorna True se o token for válido, e False caso contrário.
        """
        expiration_time = self.created_at + timedelta(hours=24)
        return timezone.now() < expiration_time

    def __str__(self):
        return f'ResetSenha para {self.user.username}'