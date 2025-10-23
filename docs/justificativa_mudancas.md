# Relatório de Mudanças e Justificativas (Etapa 1 vs. Etapa 2)

## 1. Introdução

Este documento detalha e justifica as principais mudanças implementadas na Etapa 2 (Implementação) em relação ao planejamento original e protótipos da Etapa 1 (projeto "AdoPets").

O projeto manteve integralmente seus objetivos centrais, o escopo funcional e a vinculação com o ODS 11. As alterações realizadas durante o desenvolvimento visaram aprimorar a experiência do usuário (UX), estabelecer uma identidade visual (UI) mais forte e amigável, garantir a viabilidade técnica e adicionar funcionalidades que enriqueceram a plataforma, resultando em um produto final mais robusto e completo sob o novo nome: **"A Friend for Life"**.

---

## 2. Mudanças de Design e Experiência do Usuário (UI/UX)

#### **Justificativa Geral da Evolução do Design:**

O protótipo inicial ("AdoPets") serviu como um wireframe de alta fidelidade, focando na estrutura e disposição dos elementos. Para o projeto final ("A Friend for Life"), foi desenvolvida uma identidade visual completa e coesa. A paleta de cores, centrada em tons de roxo e lilás, foi escolhida para transmitir uma sensação de cuidado, tranquilidade e afeto, temas centrais da adoção de animais. A tipografia foi refinada para melhorar a legibilidade, e elementos gráficos como o fundo de "patinhas" foram adicionados para criar uma atmosfera mais imersiva e temática, reforçando a conexão emocional com o usuário.

#### **Alterações Específicas nas Telas:**

*   **Telas de Autenticação (Cadastro, Login, Esqueci a Senha):**
    *   **O que mudou:** O layout de duas colunas foi mantido, mas a identidade visual foi completamente refeita. O lado esquerdo agora utiliza a cor primária sólida (roxo), e o lado direito apresenta uma ilustração temática que reforça a missão do projeto. O nome do projeto e o logo foram atualizados para "A Friend for Life".
    *   **Por que mudou:** A mudança cria um impacto visual imediato, estabelece a nova marca e torna a experiência de entrada no sistema mais agradável e alinhada com a proposta afetiva da plataforma.

*   **Formulários (Cadastro de Usuário e de Pet):**
    *   **O que mudou:** Os formulários foram redesenhados para maior clareza e usabilidade. No protótipo, os campos de características do pet usavam "tags" clicáveis. Na versão final, foram utilizados checkboxes e radio buttons, que são elementos de formulário mais padronizados e intuitivos para a seleção de múltiplas opções. Foi adicionada a indicação de campos obrigatórios (`*Obrigatório`) para guiar melhor o usuário.
    *   **Por que mudou:** A troca para checkboxes melhora a acessibilidade e a experiência do usuário, pois é um padrão de interação universalmente reconhecido. A indicação de obrigatoriedade reduz a chance de erros no preenchimento.

*   **Página de Listagem de Pets (Adotar):**
    *   **O que mudou:** Os cards dos pets foram completamente redesenhados. Na versão final, eles são mais ricos em informação visual: incluem ícones para espécie e sexo, a localização (cidade/estado), uma breve descrição, e um indicador visual para o tamanho do pet. A paleta de cores foi aplicada para diferenciar gênero (ícones e nomes).
    *   **Por que mudou:** O objetivo foi fornecer o máximo de informações úteis ao usuário "de relance", permitindo que ele tome decisões mais rápidas sobre em qual perfil clicar. Isso otimiza a jornada de busca e torna a interface mais informativa e visualmente agradável.

*   **Página de Detalhes do Pet ("Ver Pet"):**
    *   **O que mudou:** O layout foi completamente reestruturado para ser mais organizado e visualmente agradável. O protótipo apresentava as informações em uma única coluna. A versão final divide a página em seções claras e distintas:
        1.  Uma área de destaque com a foto principal, a galeria de imagens secundárias e as informações essenciais do pet e do protetor.
        2.  Um grid de "cards" para as características (Temperamento, Cuidados, etc.), tornando-as mais fáceis de escanear.
        3.  Uma seção dedicada e centralizada para "A História do Pet".
    *   **Por que mudou:** A nova estrutura melhora drasticamente a hierarquia da informação. O usuário consegue absorver os dados mais importantes rapidamente na primeira seção e depois explorar os detalhes de personalidade e a história do animal de forma mais focada. O uso de cards e seções separadas quebra o conteúdo, tornando a leitura menos cansativa e a experiência geral muito mais intuitiva.

*   **Página de Perfil do Usuário:**
    *   **O que mudou:** O perfil no protótipo era mais simples. A versão final apresenta um layout mais limpo, com destaque para as ações principais ("Cadastrar novo animal", "Ver contatos") e para as métricas ("Animais divulgados", "Animais adotados"). A listagem dos pets do usuário agora utiliza os mesmos cards redesenhados, com a adição dos botões "Editar" e "Remover".
    *   **Por que mudou:** O novo design organiza melhor as informações e foca nas ações que o protetor mais precisa realizar, melhorando a eficiência do gerenciamento de seus anúncios.

---

## 3. Mudanças e Adições de Funcionalidade

Durante a implementação, novas funcionalidades foram adicionadas para enriquecer a plataforma e atender a necessidades identificadas durante o desenvolvimento.

*   **Funcionalidade Adicionada: Sistema de Depoimentos (Página Completa)**
    *   **Justificativa:** O protótipo não previa uma seção de depoimentos. Foi decidido adicionar esta funcionalidade para criar "prova social" e engajamento. Permitir que usuários compartilhem suas histórias de adoção bem-sucedidas inspira confiança em novos usuários e reforça o impacto positivo da plataforma. A funcionalidade implementada permite que o usuário crie, edite e delete seu próprio depoimento.

*   **Funcionalidade Adicionada: Páginas Institucionais (App `sobre_nos`)**
    *   **Justificativa:** Páginas como "Quem Somos", "Termos de Serviço" e "Política de Privacidade" não estavam no escopo visual do protótipo inicial, mas são essenciais para qualquer aplicação web séria. Elas foram adicionadas para garantir a transparência, a credibilidade e a conformidade legal da plataforma.

*   **Funcionalidade Modificada: Fluxo de Autenticação**
    *   **Justificativa:** O fluxo de autenticação foi implementado com robustez adicional, incluindo a **confirmação de cadastro por e-mail** e um fluxo completo de **recuperação de senha**. Essas etapas, embora não detalhadas visualmente no protótipo, são cruciais para a segurança das contas dos usuários e a integridade da plataforma.

*   **Funcionalidade Adicionada: Marcar Pet como "Adotado"**
    *   **Justificativa:** No protótipo, a gestão do pet se resumia a editar ou remover. Na prática, percebeu-se a necessidade de um status intermediário. A função "Marcar como Adotado" permite que o protetor mantenha o anúncio em seu histórico, contribua para as métricas de sucesso da plataforma e informe claramente aos outros usuários que aquele pet já encontrou um lar, sem precisar apagar todo o registro.

---