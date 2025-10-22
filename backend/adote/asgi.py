# Arquivo: adote/asgi.py
# Este arquivo é o ponto de entrada para servidores web compatíveis com ASGI,
# usado para deploy assíncrono. Ele configura o ambiente e expõe a aplicação Django.

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adote.settings')
application = get_asgi_application()
``````python
# Arquivo: adote/wsgi.py
# Este arquivo é o ponto de entrada para servidores web compatíveis com WSGI,
# como o Gunicorn, usado para deploy síncrono. Ele configura o ambiente e
# expõe a aplicação Django para o servidor web.

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adote.settings')
application = get_wsgi_application()