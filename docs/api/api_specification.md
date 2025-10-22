### **Arquivo: `docs/api/api_specification.md`**

# Documento de Especificação de APIs e Interfaces

Este documento descreve as principais interfaces de comunicação e os endpoints (views) principais da plataforma "A Friend for Life".

### 1. Visão Geral da Comunicação

A plataforma utiliza uma arquitetura de renderização no servidor, onde as "APIs internas" são os endpoints de URL definidos no Django. A comunicação ocorre via requisições HTTP (GET e POST). Adicionalmente, o sistema consome APIs externas.

### 2. Endpoints da Aplicação (APIs Internas)

| Método | Endpoint (URL) | View Responsável | Parâmetros de Requisição | Formato de Resposta | Descrição da Funcionalidade |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `GET`/`POST` | `/auth/cadastro/` | `views.cadastro` | Campos do formulário (nome, e-mail, senha, etc.) | HTML | Exibe o formulário (GET) ou processa o registro do novo usuário (POST). |
| `GET`/`POST` | `/auth/login/` | `views.logar` | `email`, `senha` | HTML | Exibe o formulário (GET) ou autentica e inicia a sessão do usuário (POST). |
| `GET`/`POST` | `/auth/esqueceu_senha/` | `views.esqueceu_senha` | `email` | HTML | Exibe o formulário (GET) ou inicia o processo de recuperação de senha (POST). |
| `GET`/`POST` | `/auth/criar_senha/<uidb64>/<token>/` | `views.criar_senha` | `senha_nova`, `confirmar_senha` | HTML | Permite que o usuário defina uma nova senha após a validação do token. |
| `GET` | `/auth/confirmar_email/<uidb64>/<token>/` | `views.confirmar_email` | - | HTML (Redirecionamento) | Ativa a conta do usuário a partir do link de confirmação do e-mail. |
| `GET` | `/perfil/sair/` | `views.sair` | - | HTML (Redirecionamento) | Encerra a sessão do usuário (logout). |
| `GET`/`POST` | `/divulgar/novo_pet/` | `views.novo_pet` | Campos do formulário do pet, `foto_principal`, `fotos_secundarias` | HTML | Exibe o formulário (GET) ou cadastra um novo pet (POST). |
| `GET`/`POST` | `/divulgar/ver_pet/<id>/` | `views.ver_pet` | - | HTML | Exibe os detalhes de um pet (GET) ou marca o pet como adotado (POST). |
| `GET` | `/adotar/listar_pets/` | `views.listar_pets` | Parâmetros de filtro (`estado`, `cidade`, `tamanho`, `especie`, `page`) | HTML | Exibe a lista de pets disponíveis, aplicando os filtros fornecidos. |
| `GET` | `/perfil/meu_perfil/` | `views.meu_perfil` | - | HTML | Exibe o perfil do usuário logado. |
| `GET`/`POST` | `/perfil/editar_perfil/` | `views.editar_perfil` | Campos do formulário de perfil (nome, telefone, etc.) | HTML | Exibe o formulário (GET) ou atualiza os dados do perfil (POST). |
| `GET`/`POST` | `/perfil/alterar_senha/` | `views.alterar_senha` | `senha_atual`, `senha_nova` | HTML | Exibe o formulário (GET) ou processa a alteração de senha (POST). |
| `POST` | `/perfil/remover_conta/` | `views.remover_conta` | - | HTML (Redirecionamento) | Remove a conta do usuário. |
| `GET` | `/mais_depoimentos/` | `views.mais_depoimentos` | `pagina_atual` (query param) | JSON | Retorna uma lista paginada de depoimentos para carregamento dinâmico. |

### 3. Interfaces de Comunicação com Serviços Externos

-   **Amazon Web Services (AWS S3):**
    -   **Descrição:** O sistema se comunica com a API do Amazon S3 para todo o armazenamento de arquivos de mídia (fotos de pets e perfis).
    -   **Protocolo/Interface:** A comunicação é feita através do SDK da AWS para Python (Boto3), abstraída pela biblioteca `django-storages`. As operações principais são `PutObject` (para upload) e `GetObject` (para leitura).
    -   **Autenticação:** Requer `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY` para autorizar as operações no bucket.

-   **API de Localidades do IBGE:**
    -   **Descrição:** Consumida via requisições HTTP para popular dinamicamente os formulários de localização com estados e cidades.
    -   **Protocolo/Interface:** API REST.
    -   **Método:** `GET`.
    -   **Formato de Resposta:** JSON.
    -   **Autenticação:** Não requerida.

-   **Serviço de E-mail (SMTP):**
    -   **Descrição:** Utilizado para enviar e-mails transacionais, como confirmação de cadastro e recuperação de senha.
    -   **Protocolo/Interface:** SMTP (Simple Mail Transfer Protocol).
    -   **Autenticação:** Requerida via `EMAIL_HOST_USER` e `EMAIL_HOST_PASSWORD`.
