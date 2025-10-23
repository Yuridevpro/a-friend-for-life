# pagina_inicio/apps.py

# Este arquivo contém a configuração do app 'pagina_inicio'.
# A classe 'PaginaInicioConfig' permite ao Django identificar
# este app e suas configurações dentro do projeto.


from django.apps import AppConfig


class PaginaInicioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pagina_inicio'
