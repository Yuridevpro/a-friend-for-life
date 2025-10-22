# adotar/apps.py

# Este arquivo contém a configuração do app 'adotar'.
# A classe 'AdotarConfig' permite que o Django identifique este app
# e suas configurações dentro do projeto.

from django.apps import AppConfig
class AdotarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adotar'
