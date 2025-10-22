# pagina_inicio/models.py


# Este arquivo define os modelos de dados para o app 'pagina_inicio'.
# Ele contém o modelo 'Depoimento', que armazena as mensagens,
# nome e informações de contato dos usuários que deixaram um feedback
# na plataforma.

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from perfil.models import UserProfile

class Depoimento(models.Model):
    """
    Representa um depoimento deixado por um usuário.
    Armazena a mensagem e associa o depoimento ao usuário que o escreveu.
    """
    # O email é único para garantir que cada usuário tenha apenas um depoimento.
    # Ao tentar criar um novo, o antigo é atualizado.
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100, blank=True)
    mensagem = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='depoimentos')

    def __str__(self):
        return f"{self.nome} - {self.data_criacao.strftime('%d/%m/%Y')}"
    
    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para garantir que o nome e sobrenome
        do depoimento estejam sempre sincronizados com o perfil do usuário
        no momento de salvar.
        """
        if self.usuario:
            try:
                user_profile = UserProfile.objects.get(user=self.usuario)
                self.nome = user_profile.nome
                self.sobrenome = user_profile.sobrenome
            except UserProfile.DoesNotExist:
                # Caso o perfil não seja encontrado, usa o nome de usuário padrão.
                self.nome = self.usuario.username
        super().save(*args, **kwargs)