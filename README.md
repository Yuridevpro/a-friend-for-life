<!-- README.md -->

# 🐾 A Friend for Life - Plataforma de Adoção de Animais

Sistema web completo para conectar protetores de animais a pessoas interessadas em adoção, facilitando o encontro entre pets e seus futuros lares.

## 🚀 Acesso à Plataforma

**Acesse a aplicação em produção no seguinte link:**
### [https://um-amigo-for-life02.onrender.com/](https://um-amigo-for-life02.onrender.com/)

![Status](https://img.shields.io/badge/Status-Pronto%20para%20Deploy-brightgreen)![Versão](https://img.shields.io/badge/Versão-1.0-blue)![Python](https://img.shields.io/badge/Python-3.x-blue)![Django](https://img.shields.io/badge/Django-4.x-darkgreen)![Database](https://img.shields.io/badge/Database-PostgreSQL-blueviolet)

---

## 🎯 Problema Abordado e Objetivos

### Problema
O grande número de animais abandonados e a dificuldade de conexão entre protetores independentes/ONGs e potenciais adotantes criam um ciclo de superlotação em abrigos e sofrimento animal. Protetores lutam para dar visibilidade aos animais, enquanto pessoas que desejam adotar muitas vezes não sabem por onde começar a procurar.

### Objetivos do Sistema
*   **Centralizar e Facilitar a Adoção:** Criar um ponto de encontro digital, unificando os anúncios de pets para adoção e simplificando o processo de busca para os adotantes.
*   **Aumentar a Visibilidade:** Fornecer uma ferramenta eficaz para que protetores possam divulgar os animais sob seus cuidados para um público mais amplo.
*   **Promover a Posse Responsável:** Oferecer informações detalhadas sobre cada animal para ajudar a garantir que as adoções sejam bem-sucedidas e duradouras.
*   **Gerar Impacto Social Positivo:** Contribuir para a diminuição do número de animais abandonados e fortalecer a comunidade de proteção animal, alinhando-se ao **ODS 11 (Cidades e Comunidades Sustentáveis)**.

## 📋 Escopo do Projeto

O escopo do projeto "A Friend for Life" abrange o ciclo completo de divulgação e busca para adoção de animais:
1.  **Gerenciamento de Usuários:** Cadastro com confirmação por e-mail, login, recuperação de senha e gerenciamento de perfil.
2.  **Gerenciamento de Pets:** Protetores podem cadastrar, editar, remover e marcar pets como adotados.
3.  **Busca e Adoção:** Visitantes e usuários podem buscar pets com filtros de localização e características, além de visualizar os contatos do protetor.
4.  **Engajamento:** Usuários podem deixar depoimentos para compartilhar suas experiências.

**Fora do Escopo:** O sistema **não** lida com transações financeiras (doações), gerenciamento de estoque de abrigos ou o processo de adoção em si (entrevistas, contratos), que ocorrem diretamente entre o adotante e o protetor.

## 🏛️ Visão Geral da Arquitetura

A plataforma utiliza uma **Arquitetura Monolítica** com o framework **Django**, seguindo o padrão **Model-View-Template (MVT)**. Esta abordagem foi escolhida para simplificar o desenvolvimento e a implantação. O sistema se comunica com serviços externos para funcionalidades chave como armazenamento de mídia (AWS S3) e consulta de localização (API IBGE).

```mermaid
graph TD
    subgraph "Usuário"
        A[Visitante / Protetor]
    end

    subgraph "Infraestrutura de Produção"
        B[Browser] --> C{Load Balancer / Nginx};
        C --> D[Servidor de Aplicação - Gunicorn];
        D -- WSGI --> E((Django App<br>A Friend for Life));
        E -- ORM --> F[(PostgreSQL DB)];
        E -- boto3/storages --> G[(AWS S3<br>Armazenamento de Mídia)];
        E -- HTTP Request --> H[API Externa<br>IBGE];
        E -- SMTP --> I[Serviço de E-mail];
    end

    A -- HTTP/HTTPS --> B;

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style E fill:#bbf,stroke:#333,stroke-width:2px
```

## 🚀 Início Rápido (Ambiente de Desenvolvimento)

### 1. Pré-requisitos
- Python 3.x
- Git

### 2. Configuração do Ambiente
```bash
# Clone o repositório
git clone https://github.com/Yuridevpro/a-friend-for-life.git
cd a-friend-for-life # Navegue para a pasta clonada

# Crie e ative um ambiente virtual
python -m venv ambiente_virtual
source ambiente_virtual/bin/activate  # No Windows: ambiente_virtual\Scripts\activate

# Navegue até a pasta do backend e instale as dependências
cd backend
pip install -r requirements.txt
```

### 3. Variáveis de Ambiente
Crie um arquivo chamado `.env` dentro da pasta `backend/`.

**Configurações Mínimas para Rodar Localmente:**
Para iniciar a aplicação em seu computador, você só precisa destas duas variáveis.
```ini
# backend/.env

# Define o ambiente como desenvolvimento para usar o banco de dados SQLite e habilitar o modo DEBUG.
ENVIRONMENT='development'

# Chave de segurança do Django. Gere uma nova para seu ambiente.
SECRET_KEY='sua-chave-secreta-django'
```

**Configurações Opcionais (Para testar funcionalidades específicas):**
A aplicação funcionará sem as chaves abaixo, mas com recursos limitados.
```ini
# backend/.env (continue no mesmo arquivo)

# Opcional: Para testar o upload de imagens para o Amazon S3.
# Sem estas chaves, o upload de fotos de pets e de perfil não funcionará.
AWS_ACCESS_KEY_ID='sua_chave_aws'
AWS_SECRET_ACCESS_KEY='sua_chave_secreta_aws'
AWS_STORAGE_BUCKET_NAME='nome-do-seu-bucket-s3'
AWS_S3_REGION_NAME='us-east-1'

# Opcional (Obrigatório para Produção): Para testar o envio de e-mails para um provedor real (ex: SendGrid).
# Se estas chaves forem omitidas, os e-mails serão impressos no terminal.
SENDGRID_API_KEY='sua-chave-api-do-sendgrid'
DEFAULT_FROM_EMAIL='seu-email-verificado@exemplo.com'
```

**Configurações para Produção (Ignoradas localmente):**
Estas variáveis são usadas apenas para o deploy em produção com PostgreSQL.
```ini
# backend/.env (continue no mesmo arquivo)

# Usado apenas em ambiente de produção (quando ENVIRONMENT='production')
DB_NAME='nome_do_banco_postgres'
DB_USER='usuario_postgres'
DB_PASSWORD='senha_postgres'
DB_HOST='host_do_banco'
DB_PORT=5432```

### 4. Banco de Dados e Execução
**IMPORTANTE:** Todos os comandos `manage.py` devem ser executados de dentro da pasta `backend/`.
```bash
# Certifique-se de que você está na pasta 'backend'

# Aplique as migrações do banco de dados
python manage.py migrate

# Inicie o servidor de desenvolvimento
python manage.py runserver
```

### 5. Ativando a Conta de Usuário Localmente
Se você não configurou as variáveis de ambiente do SendGrid, os e-mails não serão enviados para sua caixa de entrada. Em vez disso, o conteúdo do e-mail, incluindo o link de ativação, será impresso no terminal onde o `runserver` está rodando.

1.  Após se cadastrar na plataforma, olhe o terminal.
2.  Você verá a saída do e-mail. Procure por um link parecido com este: `http://127.0.0.1:8000/auth/confirmar_email/MzI3/NzN2.../`
3.  Copie e cole este link no seu navegador para ativar sua conta.

### 6. Acesso
Abra seu navegador e acesse: **http://127.0.0.1:8000/**

### 🧪 Executando os Testes
Para verificar a integridade e o funcionamento das principais funcionalidades, execute a suíte de testes automatizados.

```bash
# Certifique-se de que você está na pasta 'backend'

# Execute o comando de teste
python manage.py test tests
```
O resultado esperado é a execução de todos os testes com o status **OK**.

## ✨ Funcionalidades Principais

### 👤 Para Adotantes
- **Busca Avançada:** Filtre pets por localização, espécie e tamanho.
- **Perfis Detalhados:** Veja a história, fotos e características de cada pet.
- **Contato Direto:** Acesse facilmente o contato do protetor (WhatsApp, E-mail).
- **Perfis de Protetores:** Conheça quem está cuidando do animal.

### 💖 Para Protetores
- **Cadastro de Pets:** Adicione animais para adoção com um formulário completo.
- **Galeria de Fotos:** Faça upload de múltiplas imagens para cada pet.
- **Gerenciamento de Perfil:** Edite suas informações e gerencie seus animais cadastrados.
- **Status de Adoção:** Marque seus pets como "Adotado" com um clique.

### ⚙️ Sistema Robusto
- **Autenticação Segura:** Cadastro com confirmação por e-mail e recuperação de senha.
- **Perfis Completos:** Middleware que garante que os usuários preencham seus dados.
- **Armazenamento em Nuvem:** Uso de AWS S3 para escalabilidade e segurança das imagens.
- **Interface Responsiva:** Experiência otimizada para Desktop e Mobile.

## 🎯 Casos de Uso

### 👨‍👩‍👧‍👦 Famílias
- Encontrar o pet ideal que se encaixe no estilo de vida da família (tamanho, temperamento, etc.).
- Conectar-se com protetores locais de forma segura.

### 🐕 Protetores Independentes e ONGs
- Aumentar a visibilidade dos animais resgatados.
- Gerenciar de forma centralizada todos os pets disponíveis para adoção.
- Manter a comunidade atualizada sobre o status de cada animal.

### 📚 Acadêmico (ODS 11)
- O projeto serve como um caso prático de tecnologia aplicada para resolver um problema social urbano, contribuindo para a meta do **ODS 11: Cidades e Comunidades Sustentáveis**.

## 📁 Estrutura do Projeto

```
projeto-academico-adote/
├── 📄 README.md
├── 📄 .gitignore
│
├── 📂 backend/
│   ├── 📄 manage.py
│   ├── 📜 requirements.txt
│   ├── 🔑 .env
│   ├── ⚙️ adote/
│   ├── ❤️ adotar/
│   ├── 🐶 divulgar/
│   ├── 🏠 pagina_inicio/
│   ├── 👤 perfil/
│   ├── ℹ️ sobre_nos/
│   ├── 📱 usuarios/
│   └── 📂 tests/
│
├── 📂 frontend/
│   └── 📂 web/
│       └── 🎨 templates/
│           ├── 📄 base.html
│           ├── 📂 static/
│           ├── 📂 adotar/
│           ├── 📂 divulgar/
│           └── ... (outros templates de apps)
│
├── 📂 database/
│   └── 📄 schema.sql
│
└── 📂 docs/
    ├── 📂 requirements/
    ├── 📂 architecture/
    └── ... (outros documentos)
    
```

## 🔬 Tecnologias Utilizadas

- **Backend:** Python, Django
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5, jQuery
- **Banco de Dados:** PostgreSQL (Produção), SQLite (Desenvolvimento)
- **Armazenamento:** Amazon S3
- **Infraestrutura (Produção):** Gunicorn, Nginx


## 🗓️ Cronograma de Desenvolvimento (Etapa 2)

O plano de desenvolvimento para a implementação do sistema está estruturado em um cronograma de **60 dias**, dividido em **4 Sprints** de duas semanas (10 dias úteis) cada, seguindo a metodologia Scrum.

-   **Reuniões:**
    -   **Sprint Planning:** 1º dia de cada Sprint, às 19h.
    -   **Reuniões Diárias (Daily Scrum):** Todos os dias, das 19h às 20h.
    -   **Sprint Review:** Último dia de cada Sprint, às 19h.
    -   **Sprint Retrospective:** Último dia de cada Sprint, às 20h.

---

### **Entregas - Mínimo Produto Viável (MVP)**

#### **1ª Sprint: Estrutura do Projeto e Autenticação**

*   **Configuração do Ambiente e Backend:**
    *   Configurar `settings.py` com variáveis de ambiente (`.env`) para desenvolvimento e produção.
    *   Integrar o armazenamento de mídia com o Amazon S3 utilizando `django-storages` e `boto3`.
    *   Estruturar o banco de dados PostgreSQL e aplicar as migrações iniciais.

*   **Módulo de Autenticação (`usuarios` app):**
    *   Implementar a view `cadastro` para criar instâncias dos models `User` e `UserProfile`.
    *   Desenvolver o fluxo de confirmação por e-mail, utilizando o model `Ativacao` e o serviço SMTP.
    *   Criar a view `logar` e a lógica de recuperação de senha com o model `ResetSenha`.

*   **Deploy Inicial (Homologação):**
    *   Publicar a estrutura base da aplicação em um ambiente de testes para validar a configuração inicial.

#### **2ª Sprint: Funcionalidades Essenciais de Perfil e Pets**

*   **Módulo de Perfil (`perfil` app):**
    *   Desenvolver as views `meu_perfil` e `editar_perfil`, permitindo a visualização e atualização dos dados do `UserProfile`.
    *   Implementar o `ProfileCompleteMiddleware` para garantir que os usuários completem o perfil antes de navegar.

*   **Módulo de Divulgação (`divulgar` app):**
    *   Construir a view `novo_pet` com o formulário para cadastrar instâncias do model `Pet` e `PetImage`, incluindo o upload de múltiplas imagens para o S3.
    *   Desenvolver a view `ver_pet` para exibir os detalhes de um animal e a lógica para marcá-lo como "Adotado".

*   **Deploy Incremental:**
    *   Atualizar o ambiente de homologação com as novas funcionalidades de gerenciamento de perfis e pets.

#### **3ª Sprint: Interação, Busca e Engajamento**

*   **Módulo de Adoção (`adotar` app):**
    *   Implementar a view `listar_pets` com a lógica de filtragem por localização (do `UserProfile`), espécie e tamanho.
    *   Implementar a paginação (`Paginator` do Django) para otimizar o carregamento da lista de pets.

*   **Módulo de Engajamento (`pagina_inicio` app):**
    *   Desenvolver as views para criar e gerenciar o model `Depoimento`.
    *   Implementar a view `mais_depoimentos` com `JsonResponse` para o carregamento dinâmico na `home`.

*   **Reforço de Segurança e Permissões:**
    *   Revisar todas as views críticas (`editar_pet`, `remover_pet`) para garantir que apenas o proprietário do pet possa realizar as ações.

*   **Deploy Incremental:**
    *   Atualizar o ambiente de homologação com as funcionalidades de busca e depoimentos.

#### **4ª Sprint: Validação, Refinamento e Lançamento**

*   **Testes de Aceitação e Validação (E2E):**
    *   Executar testes manuais nos principais fluxos de usuário: 1) Cadastro completo com ativação de e-mail; 2) Login, cadastro de pet e edição; 3) Busca e visualização de um pet para adoção; 4) Recuperação de senha.

*   **Refinamento da Interface (UI/UX):**
    *   Realizar ajustes finos no CSS e nos templates (`base.html` e outros) com base nos testes para garantir a responsividade e a usabilidade em diferentes dispositivos.

*   **Finalização da Documentação Técnica:**
    *   Revisar e completar todos os documentos na pasta `docs/`, incluindo o `README.md`, garantindo que toda a documentação reflita o estado final do código.

*   **Deploy Final em Produção:**
    *   Migrar a aplicação do ambiente de homologação para o ambiente de produção final.
    *   Realizar um teste piloto, convidando alguns usuários para testar a plataforma em um cenário real.
      
**Projeto desenvolvido para a disciplina de Projeto Aplicado Multiplataforma (N705).**

## 🤝 Equipe e Papéis

| Nome | Papel |
| :--- | :--- |
| José Alves Ferreira Neto | Product Owner / Gestão |
| Alan Magalhães Barros | Scrum Master |
| Alisson Rafael Silva de Almeida | Time (Desenvolvimento) |
| Yuri da Silva Ferreira | Time (Desenvolvimento) |
| Kairo César Ferreira Cunha | Time (Desenvolvimento / Testes) |
| Gabriel Nogueira Ibiapina | UX / Documentação |


---