# usuarios/urls.py

# Este arquivo define as rotas (URLs) específicas para o app 'usuarios'.
# Cada 'path' mapeia uma URL para uma função (view) correspondente no arquivo views.py.
# Isso permite que o Django saiba qual lógica executar quando um usuário acessa
# uma determinada página, como '/login/' ou '/cadastro/'.

from django.urls import path, include
from . import views



urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.logar, name='login'),
    path('esqueceu_senha/', views.esqueceu_senha, name='esqueceu_senha'),
    path('criar_senha/<uidb64>/<token>/', views.criar_senha, name='criar_senha'),
    path('confirmar_email/<uidb64>/<token>/', views.confirmar_email, name='confirmar_email'),

]