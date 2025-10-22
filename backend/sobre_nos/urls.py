# sobre_nos/urls.py


# Este arquivo define as rotas (URLs) para o app 'sobre_nos'.
# Ele mapeia cada URL, como '/quem_somos/', para a sua view correspondente
# no arquivo views.py, permitindo que os usuários acessem as páginas institucionais.

from django.urls import path
from . import views

urlpatterns = [
    path('quem_somos/', views.quem_somos, name='quem_somos'),
    path('politica_privacidade/', views.politica_privacidade, name='politica_privacidade'),
    path('termos_servico/', views.termos_servico, name='termos_servico'),
]