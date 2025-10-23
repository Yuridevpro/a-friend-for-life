# adote/urls.py


# Este é o arquivo de roteamento de URLs principal do projeto.
# Ele atua como o ponto de entrada para todas as requisições, direcionando
# cada caminho de URL para o arquivo 'urls.py' do aplicativo correspondente.
# Também configura o serviço de arquivos de mídia em ambiente de desenvolvimento.

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # Rota para a interface de administração do Django.
    path('admin/', admin.site.urls),
    
    # Inclui as rotas de cada app, organizando as URLs de forma modular.
    path('auth/', include('usuarios.urls')),
    path('divulgar/', include('divulgar.urls')),
    path('adotar/', include('adotar.urls')),
    path('perfil/', include('perfil.urls')),
    path('sobre_nos/', include('sobre_nos.urls')),
    path('pagina_inicio/', include('pagina_inicio.urls')),
    
    # Redireciona a URL raiz do site ('/') para a página inicial.
    path('', RedirectView.as_view(url='/pagina_inicio/', permanent=False)),
]

# Adiciona a configuração para servir arquivos de mídia (uploads)
# apenas em modo de desenvolvimento (DEBUG=True). Em produção, o S3 cuida disso.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)