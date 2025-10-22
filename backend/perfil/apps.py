# perfil/apps.py

# Este arquivo contém a configuração do app 'perfil'.
# A classe 'PerfilConfig' permite que o Django identifique este app
# e suas configurações, como o nome, dentro do projeto.

from django.apps import AppConfig


class PerfilConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'perfil'