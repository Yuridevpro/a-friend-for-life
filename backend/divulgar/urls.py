# divulgar/urls.py

# Este arquivo define as rotas (URLs) para o app 'divulgar'.
# Ele mapeia as URLs para as views que permitem aos usuários cadastrar,
# visualizar e editar os pets, organizando o acesso a estas funcionalidades.

from django.urls import path
from . import views

urlpatterns = [
    path('novo_pet/', views.novo_pet, name="novo_pet"),
    path('ver_pet/<int:id>', views.ver_pet, name="ver_pet"),
    path('editar_pet/<int:id>', views.editar_pet, name="editar_pet"),

]