# perfil/models.py

# Este arquivo define o modelo de dados para o app 'perfil'.
# O modelo 'UserProfile' estende o modelo de usuário padrão do Django,
# adicionando campos personalizados como nome, sobrenome, telefone,
# localização e foto de perfil. Ele usa um relacionamento OneToOneField
# para garantir que cada usuário tenha apenas um perfil.

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from storages.backends import s3boto3

# Configura o armazenamento para usar o S3 da Amazon
s3_storage = s3boto3.S3Boto3Storage()

class UserProfile(models.Model):
    """
    Representa o perfil estendido de um usuário, com informações adicionais
    que não estão no modelo User padrão do Django.
    """
    # Relacionamento um-para-um com o modelo User. Se o User for deletado, o perfil também será.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Campos para informações pessoais e de contato.
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100) # Mantém uma cópia do email para facilitar o acesso.
    
    # Campos para localização. Armazena tanto o nome quanto o ID para eficiência.
    estado_nome = models.CharField(max_length=100)
    estado_id = models.IntegerField(blank=True, null=True)
    cidade_nome = models.CharField(max_length=100)
    
    # Campo para a foto de perfil, com upload direto para o S3.
    foto_perfil = models.ImageField(upload_to='profile_pics/', storage=s3_storage, blank=True, null=True)

    def __str__(self):
        """Retorna o nome completo do usuário para representação em texto."""
        return f"{self.nome} {self.sobrenome}"