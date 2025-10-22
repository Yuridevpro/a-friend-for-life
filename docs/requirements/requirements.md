### **Arquivo: `docs/requirements/requirements.md`**

# Documento de Requisitos

Este documento detalha os requisitos funcionais e não-funcionais, regras de negócio e perfis de usuário para o sistema "A Friend for Life". O objetivo é servir como uma fonte de verdade para a equipe de desenvolvimento, garantindo que a solução atenda às necessidades dos usuários e aos objetivos do projeto.
### 1. Perfis de Usuários

Identificamos três perfis principais de usuários que interagem com o sistema:

*   **Visitante (Usuário Não Autenticado):** Qualquer pessoa que acessa a plataforma sem realizar login. Seu principal objetivo é explorar os pets disponíveis para adoção e conhecer a plataforma.
*   **Usuário Autenticado (Protetor):** Um usuário que completou o processo de cadastro e login. Este perfil pode, além das ações de um visitante, cadastrar e gerenciar seus próprios animais para adoção, gerenciar seu perfil e interagir com outras funcionalidades da plataforma.
*   **Administrador do Sistema:** Um superusuário com acesso à interface de administração do Django. É responsável por supervisionar a plataforma, gerenciar dados, usuários e garantir o bom funcionamento do sistema.

### 2. Requisitos Funcionais (RF)

Os Requisitos Funcionais descrevem o que o sistema deve fazer.

**Módulo de Autenticação e Cadastro (App: usuarios)**
*   **RF01 - Cadastro de Usuário:** O sistema deve permitir que um novo usuário se cadastre fornecendo nome, sobrenome, e-mail, telefone, localização (estado e cidade) e uma senha.
*   **RF02 - Confirmação de E-mail:** O sistema deve enviar um e-mail de confirmação para o endereço fornecido durante o cadastro. A conta do usuário só deve ser ativada após o clique no link de confirmação.
*   **RF03 - Login de Usuário:** O sistema deve permitir que um usuário cadastrado e ativo faça login utilizando seu e-mail e senha.
*   **RF04 - Logout de Usuário:** O sistema deve permitir que um usuário autenticado encerre sua sessão (logout).
*   **RF05 - Recuperação de Senha:** O sistema deve fornecer uma funcionalidade de "Esqueci minha senha" que envie um link de redefinição para o e-mail do usuário.

**Módulo de Gerenciamento de Perfil (App: perfil)**
*   **RF06 - Visualização de Perfil:** Um usuário autenticado deve poder visualizar seu próprio perfil, que exibirá suas informações, foto, contadores de pets divulgados/adotados e uma lista de seus pets cadastrados.
*   **RF07 - Edição de Perfil:** O usuário deve poder editar todas as suas informações de perfil, incluindo nome, sobrenome, e-mail, telefone, localização e foto de perfil.
*   **RF08 - Validação de Perfil Completo:** O sistema deve obrigar os usuários a preencherem todos os campos obrigatórios de seu perfil antes de poderem acessar outras funcionalidades da plataforma.
*   **RF09 - Alteração de Senha (Logado):** Um usuário autenticado deve poder alterar sua senha, fornecendo a senha atual e uma nova senha.
*   **RF10 - Remoção de Conta:** O usuário deve ter a opção de remover permanentemente sua conta da plataforma.
*   **RF11 - Visualização de Perfil de Protetor:** Qualquer usuário deve poder visualizar o perfil público de outro protetor, exibindo suas informações de contato e a lista de pets que ele divulgou.

**Módulo de Gerenciamento de Pets (Apps: divulgar, perfil)**
*   **RF12 - Cadastro de Pet:** Um usuário autenticado deve poder cadastrar um pet para adoção, fornecendo informações detalhadas como **foto principal (obrigatória)**, fotos secundárias (até 5), espécie, sexo, tamanho, nome, história e características.
*   **RF13 - Edição de Pet:** O sistema deve permitir que o proprietário de um pet edite todas as suas informações. O formulário de edição deve vir pré-preenchido com os dados atuais do animal.
*   **RF14 - Marcação de Pet como Adotado:** O proprietário do pet deve poder alterar o status de um pet de "Para adoção" para "Adotado".
*   **RF15 - Remoção de Pet:** O proprietário do pet deve poder remover (desativar) um anúncio de pet da plataforma.
*   **RF16 - Visualização de Detalhes do Pet:** Qualquer usuário deve poder visualizar a página de detalhes de um pet, com todas as suas fotos, informações, história e os dados de contato do protetor.

**Módulo de Adoção e Busca (Apps: adotar, pagina_inicio)**
*   **RF16 - Listagem de Pets:** O sistema deve exibir uma lista paginada de todos os pets ativos e disponíveis para adoção.
*   **RF17 - Filtragem de Pets:** O sistema deve permitir que os usuários filtrem a lista de pets com base na localização (estado e cidade), tamanho e espécie.
*   **RF18 - Contato com Protetor:** A página de detalhes do pet deve exibir as informações de contato do protetor (e-mail, telefone, link para WhatsApp) para facilitar o processo de adoção.

**Módulo de Conteúdo e Engajamento (App: pagina_inicio)**
*   **RF19 - Gerenciamento de Depoimentos:** Um usuário autenticado deve poder criar, editar e deletar seu próprio depoimento sobre sua experiência com a plataforma.
*   **RF20 - Carregamento Dinâmico de Depoimentos:** A página inicial deve carregar mais depoimentos dinamicamente quando o usuário solicitar, sem a necessidade de recarregar a página.

### 3. Requisitos Não-Funcionais (RNF)

Os Requisitos Não-Funcionais descrevem como o sistema deve operar.

*   **RNF01 - Segurança:** A aplicação deve ser protegida contra vulnerabilidades comuns da web, como CSRF e XSS. Todas as senhas de usuários devem ser armazenadas de forma segura (hashed).
*   **RNF02 - Usabilidade:** A interface do sistema deve ser intuitiva, responsiva e adaptar-se a diferentes tamanhos de tela (desktop, tablets e smartphones). O sistema deve fornecer feedback claro ao usuário após a realização de ações (ex: "Perfil atualizado com sucesso").
*   **RNF03 - Desempenho:** As páginas que exibem listas de pets e depoimentos devem carregar rapidamente. A paginação deve ser utilizada para evitar o carregamento de um grande volume de dados de uma só vez.
*   **RNF04 - Escalabilidade:** A arquitetura deve suportar um aumento no número de usuários e pets. O armazenamento de arquivos de mídia (fotos) deve ser feito em um serviço de armazenamento em nuvem (Amazon S3) para não sobrecarregar o servidor da aplicação.
*   **RNF05 - Manutenibilidade:** O código-fonte deve ser modular e organizado em aplicações Django distintas, facilitando futuras manutenções e a adição de novas funcionalidades.
*   **RNF06 - Compatibilidade:** A aplicação web deve ser compatível com as versões mais recentes dos principais navegadores (Google Chrome, Mozilla Firefox, Safari, Microsoft Edge).
*   **RNF07 - Disponibilidade:** A plataforma deve estar disponível para os usuários 24 horas por dia, 7 dias por semana, com um tempo de inatividade mínimo.
*   **RNF08 - Deployabilidade:** As configurações do sistema devem ser gerenciadas por variáveis de ambiente, permitindo a fácil implantação em diferentes ambientes (desenvolvimento e produção) com configurações distintas (ex: banco de dados SQLite localmente e PostgreSQL em produção).

### 4. Histórias de Usuário

*   **HU01: Como um visitante,** eu quero buscar pets por estado, cidade, espécie e tamanho, para que eu possa encontrar um animal que se encaixe no meu perfil e na minha localidade.
*   **HU02: Como um novo usuário,** eu quero me cadastrar na plataforma de forma segura e confirmar meu e-mail, para que eu possa começar a divulgar animais para adoção.
*   **HU03: Como um protetor de animais,** eu quero cadastrar um pet com fotos e informações detalhadas sobre sua história e personalidade, para aumentar suas chances de encontrar um lar adequado.
*   **HU04: Como um protetor de animais,** eu quero gerenciar meu perfil e os anúncios dos meus pets, **editando suas informações** ou marcando-os como "adotados" quando encontrarem um lar, para manter a plataforma sempre atualizada.
*   **HU05: Como um usuário que adotou um pet,** eu quero deixar um depoimento na plataforma, para compartilhar minha experiência positiva e incentivar outras pessoas a adotarem.

### **5. Regras de Negócio**

As seguintes regras de negócio governam o comportamento e as restrições da plataforma "A Friend for Life", garantindo a integridade dos dados e a qualidade da experiência do usuário.

#### **Regras de Conta e Perfil**

*   **RN01 - Integridade do Perfil do Usuário:** O sistema garante que todo usuário autenticado possua um perfil completo antes de interagir com a plataforma. Embora os dados do perfil (nome, sobrenome, telefone e localização) sejam capturados e salvos durante o **processo de cadastro**, um `middleware` de verificação atua em cada requisição. Caso o perfil do usuário seja detectado como incompleto por qualquer motivo, o acesso à página solicitada é bloqueado e ele é **automaticamente redirecionado** para a tela de "Editar Perfil" para que complete suas informações. *(Fonte: `perfil/middleware.py`, `usuarios/views.py`)*

*   **RN02 - Confirmação de E-mail para Ativação:** Uma nova conta de usuário é criada com o status "inativo". A conta só se torna funcional e permite o login após o usuário clicar no link de confirmação enviado para o seu e-mail, que possui um prazo de validade. *(Fonte: `usuarios/views.py`)*

*   **RN03 - Unicidade de E-mail:** Cada endereço de e-mail só pode ser associado a uma única conta de usuário ativa na plataforma. O sistema impede o cadastro de um e-mail já em uso. *(Fonte: `usuarios/views.py`)*

*   **RN04 - Formato de Dados do Usuário:** Os dados de e-mail e telefone fornecidos pelo usuário devem seguir formatos válidos, que são verificados no momento do cadastro e da edição do perfil. *(Fonte: `perfil/views.py` e `usuarios/views.py`)*

#### **Regras de Gerenciamento de Pets**

*   **RN05 - Propriedade do Pet:** Apenas o usuário que cadastrou um pet (o proprietário) tem permissão para editar, remover ou marcar o pet como "adotado". O sistema impede que outros usuários realizem essas ações. *(Fonte: `divulgar/views.py` e `perfil/views.py`)*

*   **RN06 - Foto Principal Obrigatória:** Todo anúncio de pet deve, obrigatoriamente, possuir uma foto principal. O sistema impede o salvamento de um novo cadastro ou de uma edição que resulte em um pet sem foto principal. *(Fonte: `divulgar/views.py`)*

*   **RN07 - Limite de Fotos Secundárias:** Um pet pode ter no máximo 5 (cinco) fotos secundárias em sua galeria. O sistema valida essa contagem tanto no cadastro de um novo pet quanto na edição de um pet existente. *(Fonte: `divulgar/views.py`)*

*   **RN08 - Campos Obrigatórios do Pet:** Todos os campos de informação do pet (nome, história, espécie, sexo, tamanho e todas as características) são de preenchimento obrigatório para garantir a qualidade e a completude dos anúncios. *(Fonte: `divulgar/views.py`)*

*   **RN09 - Visibilidade dos Anúncios:** Apenas pets com o status "Para Adoção" (`P`) e que estão marcados como ativos (`is_active=True`) são exibidos nas páginas de listagem e busca da plataforma. *(Fonte: `adotar/views.py` e `pagina_inicio/views.py`)*

#### **Regras de Conteúdo**

*   **RN10 - Depoimento Único por Usuário:** Embora um usuário possa, tecnicamente, ter múltiplos depoimentos, a lógica da aplicação trata o depoimento como único. Ao enviar um "novo" depoimento, o sistema atualiza o depoimento existente daquele usuário em vez de criar um novo registro. *(Fonte: `pagina_inicio/views.py`)*

