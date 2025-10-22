# adote/settings.py


# Este é o arquivo de configuração principal do projeto Django.
# Ele define todas as configurações globais, como a chave secreta,
# banco de dados, aplicativos instalados, middlewares, caminhos de templates
# e arquivos estáticos, além de configurações para serviços externos
# como Amazon S3 e envio de e-mails. As configurações são carregadas
# dinamicamente a partir de variáveis de ambiente para garantir segurança
# e flexibilidade entre ambientes de desenvolvimento e produção.

from pathlib import Path
import os
from django.contrib.messages import constants
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Define o diretório base do projeto (a pasta 'backend')
BASE_DIR = Path(__file__).resolve().parent.parent

# --- CONFIGURAÇÕES DE AMBIENTE E SEGURANÇA ---

# Chave secreta usada para criptografia. Lida do .env para não ser exposta no código.
SECRET_KEY = os.getenv('SECRET_KEY')

# Define o ambiente ('development' ou 'production'). O padrão seguro é 'production'.
ENVIRONMENT = os.getenv('ENVIRONMENT', 'production') 
DEBUG = (ENVIRONMENT == 'development')

# Configuração dinâmica de hosts permitidos.
if DEBUG:
    # Em desenvolvimento, permite qualquer host para facilitar os testes locais.
    ALLOWED_HOSTS = ['*']
else:
    # Em produção, restringe os hosts por segurança.
    ALLOWED_HOSTS = []
    render_hostname = os.getenv('RENDER_EXTERNAL_HOSTNAME')
    if render_hostname:
        ALLOWED_HOSTS.append(render_hostname)
    custom_hosts_str = os.getenv('ALLOWED_HOSTS')
    if custom_hosts_str:
        ALLOWED_HOSTS.extend([host.strip() for host in custom_hosts_str.split(',')])

# --- APLICAÇÕES INSTALADAS ---
# Lista de todos os apps que compõem o projeto.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usuarios',
    'divulgar',
    'adotar',
    'sobre_nos',
    'perfil',
    'pagina_inicio',
    'storages', # Para integração com S3
]

# --- MIDDLEWARE ---
# Camadas que processam as requisições e respostas globalmente.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Para servir arquivos estáticos em produção.
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'perfil.middleware.ProfileCompleteMiddleware', # Middleware personalizado.
]

# Aponta para o arquivo de URLs principal.
ROOT_URLCONF = 'adote.urls'
LOGIN_URL = '/auth/login/' # Mantenha esta linha
LOGIN_REDIRECT_URL = 'novo_pet' # Adicione esta linha (boa prática)
LOGOUT_REDIRECT_URL = 'login'  # Adicione esta linha (boa prática)

# --- TEMPLATES ---
# Configuração de onde o Django deve procurar os arquivos HTML.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '../frontend/web/templates')], # Caminho ajustado.
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuração do servidor de aplicação WSGI.
WSGI_APPLICATION = 'adote.wsgi.application'

# --- BANCO DE DADOS DINÂMICO ---
if DEBUG:
    # Em desenvolvimento, usa um arquivo SQLite3 local para simplicidade.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Em produção, usa PostgreSQL, lendo as credenciais do ambiente.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }

# --- VALIDAÇÃO DE SENHA ---
# Regras para a criação de senhas fortes.
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- INTERNACIONALIZAÇÃO ---
LANGUAGE_CODE = 'pt-BR'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# --- ARQUIVOS ESTÁTICOS (WHITENOISE) ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, '../frontend/web/templates/static')] # Caminho ajustado.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- ARQUIVOS DE MÍDIA (AMAZON S3) ---
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-east-2')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# Define o S3 como o local padrão para armazenar arquivos de upload.
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'

# --- CONFIGURAÇÃO DE E-MAIL (SENDGRID) ---
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
SENDGRID_SANDBOX_MODE_IN_DEBUG = False
SENDGRID_ECHO_TO_STDOUT = True

# --- OUTRAS CONFIGURAÇÕES ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Mapeia as tags de mensagens do Django para classes CSS do Bootstrap.
MESSAGE_TAGS = {
    constants.DEBUG: 'alert-primary',
    constants.ERROR: 'alert-danger',
    constants.SUCCESS: 'alert-success',
    constants.INFO: 'alert-info',
    constants.WARNING: 'alert-warning',
}