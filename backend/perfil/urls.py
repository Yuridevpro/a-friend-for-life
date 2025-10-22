# perfil/urls.py

# Este arquivo define as rotas (URLs) para o app 'perfil'.
# Ele mapeia cada URL relacionada ao perfil do usuário, como '/meu_perfil/'
# ou '/editar_perfil/', para a view correspondente em views.py,
# organizando como os usuários acessam as diferentes funcionalidades do perfil.

from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('meu_perfil/', views.meu_perfil, name="meu_perfil"),
    path('ver_perfil/<int:user_id>/', views.ver_perfil, name="ver_perfil"),
    path('perfil_protetor/<int:user_id>/', views.perfil_protetor, name='perfil_protetor'),
    path('editar_perfil/', views.editar_perfil, name="editar_perfil"),
    path('remover_foto_perfil/', views.remover_foto_perfil, name='remover_foto_perfil'),
    path('alterar_senha/', views.alterar_senha, name="alterar_senha"),
    path('remover_pet/<int:id>', views.remover_pet, name="remover_pet"),
    path('remover_conta/', views.remover_conta, name='remover_conta'),
    path('sair/', views.sair, name="sair"),

]



