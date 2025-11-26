# backend/src/adote/settings.py (VERSÃO FINAL COM AJUSTE NA PASTA STATIC)

from pathlib import Path
import os
from django.contrib.messages import constants
from dotenv import load_dotenv

# --- DEFINIÇÃO DE CAMINHOS ---

# O arquivo settings.py está em: backend/src/adote/
# SRC_DIR aponta para: backend/src/
SRC_DIR = Path(__file__).resolve().parent.parent
# BACKEND_DIR aponta para: backend/
BACKEND_DIR = SRC_DIR.parent
# BASE_DIR (ou ROOT_DIR) aponta para a raiz do projeto: projeto-academico-final/
BASE_DIR = BACKEND_DIR.parent

# Carrega as variáveis de ambiente do arquivo .env que está na pasta backend/
load_dotenv(BACKEND_DIR / '.env')


# --- CONFIGURAÇÕES DE AMBIENTE E SEGURANÇA ---
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# --- APLICAÇÕES INSTALADAS ---
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
    'storages',
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'perfil.middleware.ProfileCompleteMiddleware',
]

# --- URLs E REDIRECIONAMENTOS ---
ROOT_URLCONF = 'adote.urls'
LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = 'novo_pet'
LOGOUT_REDIRECT_URL = 'login'

# --- TEMPLATES ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Caminho absoluto para a pasta de templates
        'DIRS': [BASE_DIR / 'frontend/web/src/templates'],
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

WSGI_APPLICATION = 'adote.wsgi.application'



DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            # O db.sqlite3 será criado na pasta 'backend/src/'
            'NAME': SRC_DIR / 'db.sqlite3',
        }
    }


# --- VALIDAÇÃO DE SENHA ---
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
# ***** ALTERAÇÃO REALIZADA AQUI *****
# Caminho ajustado para a pasta 'public', conforme estrutura do professor.
STATICFILES_DIRS = [BASE_DIR / 'frontend/web/public/static'] # A pasta de coleta de estáticos será criada na raiz do projeto
STATIC_ROOT = BASE_DIR / 'staticfiles_build'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- ARQUIVOS DE MÍDIA (AMAZON S3) ---
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-east-2')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'

# --- CONFIGURAÇÃO DE E-MAIL (SENDGRID / CONSOLE) ---
if DEBUG:
    # Em desenvolvimento, não tente enviar e-mails de verdade.
    # Em vez disso, imprima todo o conteúdo do e-mail no console.
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # Em produção, use o backend do SendGrid para enviar e-mails reais.
    EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
    # As configurações abaixo do SendGrid são usadas apenas quando EMAIL_BACKEND é o do SendGrid.
    SENDGRID_SANDBOX_MODE_IN_DEBUG = False
    SENDGRID_ECHO_TO_STDOUT = True # Pode ser mantido, mas não terá efeito com o console.EmailBackend

# --- OUTRAS CONFIGURAÇÕES ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MESSAGE_TAGS = {
    constants.DEBUG: 'alert-primary',
    constants.ERROR: 'alert-danger',
    constants.SUCCESS: 'alert-success',
    constants.INFO: 'alert-info',
    constants.WARNING: 'alert-warning',
}