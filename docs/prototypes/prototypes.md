### **Arquivo: `docs/prototypes/prototypes.md`**


# Documento de Prototipação: A Friend for Life

Este documento detalha o processo de prototipação da interface do usuário (UI) para a plataforma, abrangendo desde os wireframes até os protótipos de alta fidelidade e a validação dos fluxos de usuário.

### Design e Protótipo do Projeto

O processo de design e a prototipagem da interface foram desenvolvidos utilizando o Figma. O link abaixo fornece acesso ao projeto completo, desde os wireframes de baixa fidelidade até o design final da interface do usuário.

[Veja os protótipos do projeto no Figma](https://www.figma.com/design/uG2MdnS6IGXu40bu2VWdhV/AdoPets---Website--Community-?node-id=10-2&p=f)

Para uma melhor compreensão da evolução do design, recomendamos navegar entre as diferentes páginas dentro do arquivo no Figma. No painel esquerdo, você encontrará seções dedicadas aos **Wireframes** e ao **UI Design** final.

#### Nota sobre a Evolução do Projeto

É importante observar que o protótipo disponível no Figma representa a fase conceitual inicial do projeto, que na época era chamado de **AdoPets**. A plataforma, em sua versão atual sob o nome **A Friend for Life**, passou por um processo de desenvolvimento iterativo.

Durante esse ciclo, diversas melhorias e adaptações foram implementadas com base no feedback de usuários e em novas demandas técnicas. Isso resultou em diferenças visuais na interface e na própria identidade do projeto.

Apesar dessas modificações, a arquitetura conceitual e as funcionalidades principais que foram validadas no protótipo, como o fluxo de cadastro, a busca por perfis e a interação na comunidade, permaneceram como a espinha dorsal do sistema final. O protótipo deve, portanto, ser visto como o ponto de partida e a visão fundamental que guiou todo o desenvolvimento subsequente.

### 1. Elaboração de Wireframes (Protótipos de Baixa Fidelidade)

A fase inicial consistiu na criação de wireframes para definir a estrutura das seis telas principais do sistema, focando na funcionalidade e na experiência do usuário (UX).

- **Wireframe 1: Página Inicial (`home.html`)**
  - **[Blocos]**: Header, Formulário de Filtro, Grid de Pets, Paginação, Seções Informativas, Depoimentos, Footer.

- **Wireframe 2: Página de Listagem de Pets (`listar_pets.html`)**
  - **[Blocos]**: Header, Formulário de Filtro, Grid de Pets (área principal), Paginação, Footer.

- **Wireframe 3: Página de Detalhes do Pet (`ver_pet.html`)**
  - **[Blocos]**: Header, Galeria de Imagens, Coluna de Informações Essenciais (contato, etc.), Seção de Detalhes, Bloco de História, Botão de Ação, Footer.

- **Wireframe 4: Página de Cadastro de Usuário (`cadastro.html`)**
  - **[Blocos]**: Painel Esquerdo com Formulário (Logo, Título, Campos de Input para dados pessoais, localização e senha), Botão "Salvar". Painel Direito com Imagem de branding.

- **Wireframe 5: Página de Cadastro de Novo Pet (`novo_pet.html`)**
  - **[Blocos]**: Header, Título da Página ("Novo Pet"), Formulário com Múltiplas Seções (Upload de Imagens, Dados Básicos do pet, Características), Botão de "Cadastrar", Footer.


- **Wireframe 6: Página de Perfil do Usuário (`meu_perfil.html`)**
  - **[Blocos]**: Header, Seção de Informações do Perfil (Foto, Nome, Localização, Contadores, Botões de Ação), Seção "Meus Pets" com Grid de Cards, Paginação para os pets, Footer.

### 2. Criação de Protótipos de Interface (Alta Fidelidade)

Após a validação da estrutura, foram desenvolvidos os protótipos de alta fidelidade, aplicando a identidade visual da marca. Os próprios arquivos de template do projeto (`.html` e `.css`) servem como protótipos funcionais.

**Identidade Visual:**
- **Paleta de Cores:** Combina tons neutros com cores de destaque para ações e informações importantes.
- **Tipografia:** Fontes claras e legíveis para garantir a boa leitura.
- **Componentes:** Uso do framework Bootstrap 5 para consistência e responsividade.

**Telas Principais Prototipadas:**
*(Instrução: Insira aqui as capturas de tela das páginas correspondentes do seu projeto em execução para ilustrar os protótipos de alta fidelidade).*

- **Tela 1: Página Inicial (`home.html`)**
  - (Inserir captura de tela da página inicial)

- **Tela 2: Listagem de Pets (`listar_pets.html`)**
  - (Inserir captura de tela da página de adoção)

- **Tela 3: Detalhes do Pet (`ver_pet.html`)**
  - (Inserir captura de tela da página de um pet específico)

- **Tela 4: Cadastro de Usuário (`cadastro.html`)**
  - (Inserir captura de tela da página de registro de novo usuário)

- **Tela 5: Cadastro de Novo Pet (`novo_pet.html`)**
  - (Inserir captura de tela do formulário de cadastro de pet)

- **Tela 6: Perfil do Usuário (`meu_perfil.html`)**
  - (Inserir captura de tela da página de perfil do usuário logado)

### 3. Validação de Fluxos de Usuário

Os protótipos de alta fidelidade foram utilizados para validar os principais fluxos de interação do usuário, garantindo que as jornadas para completar tarefas-chave fossem intuitivas e eficientes.

**Fluxo 1: Jornada de Adoção (Visitante)**

1. **Início:** O usuário acessa a Página Inicial (`home.html`).
2. **Ação:** Utiliza o formulário de filtro para buscar por pets com base em sua localização e preferências.
3. **Resultado:** O sistema exibe a página de listagem (`listar_pets.html`) com os resultados filtrados.
4. **Ação:** O usuário clica no card de um pet que lhe interessa.
5. **Resultado:** O sistema exibe a página de detalhes do pet (`ver_pet.html`).
6. **Ação:** O usuário lê os detalhes e decide entrar em contato, clicando no botão "Adotar".
7. **Resultado:** Um modal é exibido com as informações de contato do protetor, permitindo que o usuário inicie a comunicação fora da plataforma.  
**Validação:** O fluxo é considerado validado, pois permite que um visitante encontre um pet e obtenha os meios para contatar o responsável pela adoção de forma clara e direta.

**Fluxo 2: Jornada do Protetor (Do Cadastro ao Anúncio do Pet)**

1. **Início:** Um novo usuário (protetor) acessa a plataforma e clica em "Cadastre-se".
2. **Ação:** O usuário preenche o formulário de registro (`cadastro.html`).
3. **Resultado:** O sistema valida os dados e envia um e-mail de confirmação.
4. **Ação:** O usuário clica no link de confirmação em seu e-mail e realiza o login.
5. **Ação:** Já autenticado, clica em "Novo Pet".
6. **Resultado:** O sistema exibe o formulário de cadastro de pet (`novo_pet.html`).
7. **Ação:** O usuário preenche todos os campos sobre o animal e faz o upload das imagens.
8. **Ação:** Clica no botão "Cadastrar".
9. **Resultado:** O sistema valida os dados, salva o pet, armazena as imagens no S3, exibe uma mensagem de sucesso e redireciona o usuário.  
**Validação:** O fluxo é considerado validado, pois guia o novo usuário desde a criação da conta até a publicação bem-sucedida de seu primeiro anúncio, com feedback claro em cada etapa.
