# Relatório de Mudanças e Justificativas (Etapa 1 vs. Etapa 2)

## 1. Introdução

Este documento detalha e justifica as principais mudanças implementadas na Etapa 2 (Implementação) em relação ao planejamento original e protótipos da Etapa 1 (projeto "AdoPets").

O projeto manteve integralmente seus objetivos centrais e o escopo funcional, evoluindo significativamente com base no feedback do público-alvo e na necessidade de garantir a viabilidade técnica. As alterações visaram aprimorar a experiência do usuário (UX), estabelecer uma identidade visual (UI) mais forte, e adicionar funcionalidades que enriqueceram a plataforma, resultando em um produto final mais robusto e completo sob o novo nome: **"A Friend for Life"**.

---

## 2. Mudanças de Design e Experiência do Usuário (UI/UX)

#### **Justificativa Geral da Evolução do Design:**

O protótipo inicial ("AdoPets") servia como um wireframe funcional, com um design sóbrio e focado na estrutura. Durante a validação, um feedback recorrente foi o desejo por uma identidade mais acolhedora. Como sugerido por uma participante, a primeira versão parecia "um pouco ruim de ver as coisas".

Acolhendo essa crítica, o projeto final "A Friend for Life" desenvolveu uma identidade visual completa. A paleta de cores foi alterada do azul marinho para tons de **roxo e lilás**, escolhidos para transmitir cuidado e afeto. A validação posterior confirmou o sucesso dessa mudança: **100% dos respondentes** avaliaram que a nova identidade visual reflete bem a proposta de adoção. Elementos gráficos, como o fundo de "patinhas", foram adicionados para criar uma atmosfera imersiva, reforçando a conexão emocional com o usuário.

#### **Alterações Específicas nas Telas:**

*   **Telas de Autenticação (Cadastro, Login, etc.):**
    *   **O que mudou:** O layout de duas colunas foi mantido, mas a identidade visual foi completamente refeita com a nova paleta de cores e uma ilustração temática que reforça a missão do projeto.
    *   **Por que mudou:** A mudança cria um impacto visual imediato, estabelece a nova marca e torna a experiência de entrada no sistema mais agradável, alinhada com a proposta afetiva validada pelo público. O processo de cadastro foi avaliado como "eficiente" por **87,5%** dos usuários no formulário de feedback.

*   **Formulários (Cadastro de Usuário e de Pet):**
    *   **O que mudou:** Os formulários foram redesenhados para maior clareza. As "tags" clicáveis do protótipo para as características do pet foram substituídas por **checkboxes**. Foi adicionada a indicação de campos obrigatórios (`*Obrigatório`).
    *   **Por que mudou:** A troca para checkboxes melhora a acessibilidade e a usabilidade, pois é um padrão de interação universal. Embora uma protetora tenha questionado a quantidade de dados, a maioria dos adotantes (87,5%) considerou que "a plataforma oferece informações suficientes", validando a decisão de manter os campos detalhados para garantir um "match" mais responsável.

*   **Página de Listagem e Detalhes do Pet:**
    *   **O que mudou:** Os cards e a página de detalhes foram redesenhados para incluir mais informações visuais rápidas (ícones de gênero/espécie, indicadores de tamanho, etc.). A estrutura da página de detalhes foi dividida em seções claras (Informações, Contatos, Personalidade, História).
    *   **Por que mudou:** A mudança foi validada pelo feedback: **87,5%** dos usuários concordaram que as informações sobre os animais estão "bem organizadas e acessíveis". O novo layout permite que o usuário absorva os dados importantes rapidamente antes de decidir entrar em contato.

*   **Página de Perfil do Usuário:**
    *   **O que mudou:** O design foi limpo, com destaque para as ações principais ("Cadastrar novo animal") e métricas de sucesso ("Animais adotados"). Os botões "Editar" e "Remover" foram adicionados aos cards dos pets.
    *   **Por que mudou:** O novo design foca nas ações que o protetor precisa realizar, melhorando a eficiência do gerenciamento de seus anúncios.

---

## 3. Mudanças e Adições de Funcionalidade (Baseadas em Feedback)

A implementação não apenas seguiu o plano, mas também incorporou novas funcionalidades que surgiram da interação com os usuários e da maturação do projeto.

*   **Funcionalidade Adicionada: Sistema de Depoimentos (Página Completa)**
    *   **Justificativa:** Esta funcionalidade não existia no protótipo. Foi adicionada para criar "prova social". A validação confirmou sua importância: **75%** dos usuários sentiram que a plataforma transmite "confiança e segurança", e os depoimentos contribuem para essa percepção. A sugestão de evoluir para um sistema de "estrelas ou curtidas" foi anotada para futuras versões.

*   **Funcionalidade Adicionada: Páginas Institucionais (App `sobre_nos`)**
    *   **Justificativa:** Páginas como "Quem Somos", "Termos de Serviço" e "Política de Privacidade" foram adicionadas para garantir a transparência e credibilidade da plataforma, elementos essenciais para um projeto que lida com a confiança de seus usuários.

*   **Funcionalidade Modificada: Fluxo de Autenticação Completo**
    *   **Justificativa:** O fluxo de autenticação foi implementado com **confirmação por e-mail** e **recuperação de senha**. Embora não detalhadas visualmente no protótipo, são cruciais para a segurança das contas, um ponto valorizado pelos usuários na pesquisa.

*   **Funcionalidade Adicionada: Marcar Pet como "Adotado"**
    *   **Justificativa:** No protótipo, a gestão se resumia a editar/remover. A função "Marcar como Adotado" foi adicionada como uma necessidade prática para protetores, permitindo-lhes manter um histórico de sucesso e informar claramente o status do animal.

*   **Funcionalidade Planejada: Sistema de Recomendação**
    *   **Justificativa:** Durante a validação, uma *key user* sugeriu um sistema de recomendação de pets semelhantes. Embora não implementada nesta versão por extrapolar o escopo inicial, a sugestão foi registrada e validada como uma melhoria prioritária para o futuro, mostrando que o projeto está aberto à evolução contínua baseada no feedback do usuário.

---