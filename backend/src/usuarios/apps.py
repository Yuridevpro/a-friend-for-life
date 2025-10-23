# usuarios/apps.py

# Este arquivo contém a configuração do app 'usuarios'.
# A classe 'UsuariosConfig' permite que o Django identifique este app
# e suas configurações, como o nome e o tipo de campo padrão para chaves primárias.

from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'