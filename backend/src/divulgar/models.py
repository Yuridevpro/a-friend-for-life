# divulgar/models.py


# Este arquivo define os modelos de dados para o app 'divulgar'.
# Contém a classe 'Pet', que é a entidade principal do sistema, representando
# um animal para adoção, e a classe 'PetImage', para armazenar as fotos
# secundárias associadas a cada pet.

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from storages.backends import s3boto3

# Configura o armazenamento para usar o S3 da Amazon
s3_storage = s3boto3.S3Boto3Storage()


class Pet(models.Model):
    """
    Representa um animal disponível para adoção.
    Este modelo armazena todas as informações do pet, desde dados básicos
    como espécie e nome, até detalhes de personalidade e saúde.
    """
    # Opções pré-definidas para campos de múltipla escolha, garantindo a consistência dos dados.
    choices_status = (('P', 'Para adoção'), ('A', 'Adotado'))
    choices_especie = (('Cachorro', 'Cachorro'), ('Gato', 'Gato'))
    choices_sexo = (('Macho', 'Macho'), ('Fêmea', 'Fêmea'))
    choices_tamanho = (('Grande', 'Grande'), ('Médio', 'Médio'), ('Pequeno', 'Pequeno'))
    # As características são armazenadas como JSONField, permitindo uma lista flexível de tags.
    choices_cuidados_veterinarios = (
        ('Castrado', 'Castrado'),
        ('Precisa de cuidados especiais', 'Precisa de cuidados especiais'),
        ('Vacinado', 'Vacinado'),
        ('Vermifugado', 'Vermifugado')
    )
    choices_vive_bem_em = (
        ('Apartamento', 'Apartamento'),
        ('Casa com quintal', 'Casa com quintal'),
        ('Dentro de casa', 'Dentro de casa')
    )
    choices_temperamento = (
        ('Agressivo', 'Agressivo'),
        ('Arisco', 'Arisco'),
        ('Brincalhão', 'Brincalhão'),
        ('Calmo', 'Calmo'),
        ('Carente', 'Carente'),
        ('Docil', 'Docil')
    )
    choices_sociavel_com = (
        ('Cachorros', 'Cachorros'),
        ('Crianças', 'Crianças'),
        ('Desconhecidos', 'Desconhecidos'),
        ('Gatos', 'Gatos')
    )

    # Campos do modelo
    nome_pet = models.CharField(max_length=10, help_text='Nome do Pet (máximo de 10 caracteres)')
    # Chave estrangeira que liga o pet ao usuário que o cadastrou.
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=None) 
    historia_pet = models.TextField(default='História do Pet não fornecida')
    status = models.CharField(max_length=1, choices=choices_status, default='P')
    especie = models.CharField(max_length=10, choices=choices_especie)
    sexo = models.CharField(max_length=10, choices=choices_sexo)
    tamanho = models.CharField(max_length=10, choices=choices_tamanho)
    
    # JSONField é usado para armazenar listas de características selecionadas no formulário.
    cuidados = models.JSONField(default=list, blank=True)
    vive_bem_em = models.JSONField(default=list, blank=True)
    temperamento = models.JSONField(default=list, blank=True)
    sociavel_com = models.JSONField(default=list, blank=True)
    
    # Imagens com upload para o S3.
    foto_principal = models.ImageField(upload_to='pet_images/', storage=s3_storage, null=True, blank=True)
    # Relacionamento Muitos-para-Muitos com o modelo PetImage para a galeria de fotos.
    fotos_secundarias = models.ManyToManyField('PetImage', blank=True, related_name='secondary_images')
    
    telefone = models.CharField(max_length=20, null=True, blank=True)
    # Flag para "remoção lógica" (soft delete). Em vez de apagar, apenas desativamos o anúncio.
    is_active = models.BooleanField(default=True)
    # Data de criação do registro, preenchida automaticamente.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_pet


@receiver(post_save, sender=Pet)
def update_pet_location(sender, instance, created, **kwargs):
    """
    Este "signal receiver" é executado logo após um novo Pet ser criado ('created=True').
    Ele copia automaticamente a localização (estado/cidade) e o telefone do perfil
    do usuário para o registro do pet, garantindo que a informação de contato
    esteja sempre associada ao anúncio.
    """
    if created:
        instance.estado = instance.usuario.userprofile.estado_nome
        instance.cidade = instance.usuario.userprofile.cidade_nome
        instance.telefone = instance.usuario.userprofile.telefone
        instance.save()


class PetImage(models.Model):
    """
    Modelo para armazenar as imagens secundárias de um pet.
    Cada imagem é um registro separado, ligado ao pet correspondente
    através de uma chave estrangeira.
    """
    pet = models.ForeignKey(Pet, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='pet_images/secondary/', storage=s3_storage)

    def __str__(self):
        return f"Image for {self.pet.nome_pet}"