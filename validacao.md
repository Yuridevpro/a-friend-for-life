### **Guia Completo para Teste de Aceitação da Plataforma "A Friend for Life"**

Este documento serve como um roteiro para a instalação e teste completo da aplicação, simulando o processo que um avaliador realizaria.

### **1. Checklist de Requisitos Atendidos**

Antes de iniciar os testes, vamos confirmar os principais requisitos que foram cumpridos, conforme a proposta da disciplina: (olhar o doc da disciplina e fazer o checklist)

Daqui em diante, tudo é importante, pois teremos a certeza de que tudo funcionará corretamente.

### **2. Guia de Instalação do Ambiente de Desenvolvimento**

Estas são as instruções para configurar e executar o projeto em uma máquina local.

#### **2.1. Pré-requisitos**
*   Python 3.x
*   Git

#### **2.2. Configuração do Ambiente**
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

#### **2.3. Variáveis de Ambiente**
Crie um arquivo chamado `.env` na pasta `backend/`. Para rodar o projeto localmente, copie e cole o conteúdo abaixo.

**Configuração para Desenvolvimento Local:**
```ini
# --- CONFIGURAÇÕES MÍNIMAS PARA RODAR LOCALMENTE ---
ENVIRONMENT='development'
SECRET_KEY='django-insecure-academic-test-key-for-local-use-only'

# --- CONFIGURAÇÕES OPCIONAIS PARA TESTAR RECURSOS ---

# Opcional: Para testar o upload de imagens para o Amazon S3.
# AWS_ACCESS_KEY_ID='sua_chave_aws'
# AWS_SECRET_ACCESS_KEY='sua_chave_secreta_aws'
# AWS_STORAGE_BUCKET_NAME='nome-do-seu-bucket-s3'
# AWS_S3_REGION_NAME='us-east-1'

# Opcional: Para o envio de e-mails para um provedor real (ex: SendGrid).
# Se omitido, os e-mails serão impressos no terminal.
# SENDGRID_API_KEY='sua-chave-api-do-sendgrid'
# DEFAULT_FROM_EMAIL='seu-email-verificado@exemplo.com'
```

#### **2.4. Banco de Dados e Execução**
**IMPORTANTE:** Todos os comandos `manage.py` devem ser executados de dentro da pasta `backend/src/`.
```bash
# Navegue até a pasta do código-fonte
cd backend/src

# Crie o banco de dados e aplique as migrações
python manage.py migrate

# Inicie o servidor de desenvolvimento
python manage.py runserver
```

Após esses passos, a aplicação estará rodando em **`http://127.0.0.1:8000/`**.

---

### **3. Roteiro de Testes Manuais (Frontend)**

Depois que trouxe o projeto pra maquina da para realizar alguns testes como esses abaixo

#### **Fluxo 1: Autenticação e Cadastro**

**1.1 - Teste de Cadastro (Caminho Feliz):**
*   Acesse a página inicial e clique em "Cadastre-se".
*   Preencha todos os campos do formulário com dados válidos. Use um e-mail real para o qual você tenha acesso.
*   Clique em "SALVAR".
*   **Resultado Esperado:** Você deve ser redirecionado para a página de login com uma mensagem de sucesso, informando que um e-mail de confirmação foi enviado.

**1.2 - Ativação da Conta:**
*   Verifique o terminal onde o `runserver` está rodando.
*   Encontre e copie o link de confirmação de e-mail (ex: `http://127.0.0.1:8000/auth/confirmar_email/...`).
*   Cole o link no navegador.
*   **Resultado Esperado:** Você deve ser redirecionado para a página de login com uma mensagem de sucesso confirmando a ativação.

**1.3 - Teste de Login Pós-Cadastro (Caminho Feliz):**
*   Na página de login, insira o e-mail e a senha do usuário que você acabou de criar e ativar.
*   Clique em "ENTRAR".
*   **Resultado Esperado:** Você deve ser redirecionado **diretamente para a página "Novo Pet"** com uma mensagem de boas-vindas. Isso confirma que o `UserProfile` foi criado corretamente durante o cadastro e que o middleware não bloqueou o acesso.

**1.4 - Teste de Validações no Cadastro:**
*   Volte para a página de cadastro e tente se registrar:
    *   Deixando um campo obrigatório em branco.
    *   Com senhas que não coincidem.
    *   Com um formato de e-mail inválido.
*   **Resultado Esperado:** Em cada caso, a página deve recarregar mostrando uma mensagem de erro clara e específica.

**1.5 - Teste "Esqueci a Senha":**
*   Na página de login, clique em "Esqueceu a senha?".
*   Digite o e-mail do seu usuário de teste e clique em "Enviar".
*   Verifique o terminal para encontrar o link de redefinição de senha.
*   Acesse o link e crie uma nova senha.
*   **Resultado Esperado:** O fluxo deve ser concluído com uma mensagem de sucesso, e você deve conseguir fazer login com a nova senha.

#### **Fluxo 2: Gerenciamento de Perfil (Usuário Logado)**


**2.1 - Navegação Pós-Perfil Completo:**
*   Em Meu Perfil, tente navegar para outras páginas, como "Adotar" ou "Novo Pet".
*   **Resultado Esperado:** Voce será redirecionados as devidas paginas

**2.2 - Editar Perfil e Foto:**
*   Acesse "Editar Perfil" novamente.
*   Altere alguns dados (como o telefone) e adicione uma foto de perfil. Salve.
*   **Resultado Esperado:** As informações na página "Meu Perfil" e no topo da navegação (ícone de perfil) devem ser atualizadas.

#### **Fluxo 3: Gerenciamento de Pets (Usuário Logado)**

**3.1 - Cadastrar um Novo Pet:**
*   Acesse a página "Novo Pet".
*   Preencha o formulário completo, incluindo uma foto principal e algumas fotos secundárias.
*   Clique em "Cadastrar".
*   **Resultado Esperado:** Você deve ser redirecionado para a lista de pets com uma mensagem de sucesso.

**3.2 - Verificar o Pet Cadastrado:**
*   Vá para a página "Meu Perfil".
*   **Resultado Esperado:** O novo pet deve aparecer na lista "Meus Pets", e o contador "Animais divulgados" deve ser "1".

**3.3 - Editar o Pet:**
*   No card do pet em "Meu Perfil", clique em "EDITAR".
*   Altere alguma informação (ex: a história) e salve.
*   **Resultado Esperado:** As alterações devem ser salvas com sucesso.

**3.4 - Marcar Pet como Adotado:**
*   Acesse a página de detalhes do seu pet.
*   Clique no botão "Marcar Pet como Adotado".
*   **Resultado Esperado:** O status do pet deve mudar para "Adotado" na página. Em "Meu Perfil", o contador "Animais divulgados adotados" deve ser "1".

#### **Fluxo 4: Adoção e Visualização (Qualquer Usuário)**

**4.1 - Listagem e Filtragem:**
*   Acesse a página "Adotar".
*   Use os filtros (Estado, Cidade, Espécie, Tamanho) para refinar a busca.
*   **Resultado Esperado:** A lista de pets deve ser atualizada dinamicamente de acordo com os filtros aplicados.

**4.2 - Visualização de Detalhes:**
*   Clique em um pet da lista para ver sua página de detalhes.
*   **Resultado Esperado:** Todas as informações, galeria de fotos e detalhes de contato do protetor devem ser exibidos corretamente.

**4.3 - Visualização de Perfil do Protetor:**
*   Na página de detalhes do pet, clique em "Ver perfil do Protetor".
*   **Resultado Esperado:** Você deve ser levado à página de perfil público daquele usuário.

#### **Fluxo 5: Engajamento e Conteúdo**

**5.1 - Sistema de Depoimentos:**
*   Logado, acesse a página "Depoimentos".
*   Escreva e envie um depoimento.
*   **Resultado Esperado:** O depoimento deve ser salvo. Edite-o e depois delete-o, verificando se cada ação funciona.

**5.2 - Páginas Institucionais:**
*   No rodapé, clique nos links "Quem somos", "Termos de serviço" e "Política de privacidade".
*   **Resultado Esperado:** Cada link deve levar à página de conteúdo correspondente.

**6 - testar o design em telas mobile**

