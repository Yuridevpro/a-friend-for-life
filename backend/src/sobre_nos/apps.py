# sobre_nos/apps.py


# Este arquivo contém a configuração do app 'sobre_nos'.
# A classe 'SobreNosConfig' permite ao Django identificar este app
# e suas configurações dentro do projeto.

from django.apps import AppConfig


class SobreNosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sobre_nos'
