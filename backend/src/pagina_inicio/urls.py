# pagina_inicio/urls.py

# Este arquivo define as rotas (URLs) para o app 'pagina_inicio'.
# Ele mapeia a URL raiz ('/') para a view da página inicial e define as
# rotas para o gerenciamento de depoimentos, incluindo o endpoint para
# carregamento dinâmico.

from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('depoimento/', views.criar_depoimento, name='depoimento'),
    path('depoimento/<int:pk>/editar/', views.editar_depoimento, name='editar_depoimento'),
    path('depoimento/<int:pk>/deletar/', views.deletar_depoimento, name='deletar_depoimento'),
    path('mais_depoimentos/', views.mais_depoimentos, name='mais_depoimentos'),  # Adicione esta rota
    path('', views.home, name='home'),  # adicione a URL desejada
    
]

