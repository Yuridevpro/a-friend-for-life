# adotar/urls.py

# Este arquivo define as rotas (URLs) para o app 'adotar'.
# Ele contém o mapeamento da URL '/listar_pets/' para a view correspondente,
# que é a principal funcionalidade deste app, permitindo aos usuários
# encontrar animais para adoção.

from django.urls import path
from .views import listar_pets
from . import views

urlpatterns = [

    path('listar_pets/', listar_pets, name='listar_pets'),
    
]