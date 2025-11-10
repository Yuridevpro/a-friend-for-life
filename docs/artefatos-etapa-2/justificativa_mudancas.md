# Relatório de Mudanças e Justificativas (Etapa 1 vs. Etapa 2)

## 1. Introdução

Este documento detalha e justifica as principais mudanças implementadas na Etapa 2 (Implementação do projeto "A Friend for Life") em relação ao planejamento original e protótipos da Etapa 1 (projeto "AdoPets").

O projeto manteve integralmente seus objetivos centrais, o escopo funcional e a vinculação com o ODS 11. As alterações realizadas durante o desenvolvimento não foram aleatórias, mas sim o resultado de um processo iterativo que visou aprimorar a experiência do usuário (UX), estabelecer uma identidade visual (UI) mais forte, garantir a viabilidade técnica e incorporar funcionalidades que surgiram como necessidades claras durante a fase de validação, resultando em um produto final mais robusto e centrado no usuário.

---

## 2. Mudanças de Design e Experiência do Usuário (UI/UX)

#### **Justificativa Geral da Evolução do Design:**

O protótipo inicial ("AdoPets") serviu como um wireframe funcional, com um design sóbrio (azul marinho e branco) focado na estrutura. Durante a fase de elicitação e validação, um feedback qualitativo importante foi a percepção de que faltava "uma identidade da plataforma, algo que precisaria deixar o sistema mais interessante de usar".

Acolhendo essa crítica, o projeto final "A Friend for Life" desenvolveu uma identidade visual completa. A paleta de cores foi alterada para **tons de roxo e lilás**, escolhidos para transmitir cuidado, tranquilidade e afeto. A validação posterior confirmou o sucesso dessa mudança: **100% dos respondentes** avaliaram que a nova identidade visual reflete bem a proposta de adoção. Elementos gráficos, como o fundo de "patinhas", foram adicionados para criar uma atmosfera imersiva, reforçando a conexão emocional com o usuário.

#### **Alterações Específicas nas Telas:**

*   **Telas de Autenticação (Cadastro, Login, etc.):**
    *   **O que mudou:** O layout de duas colunas foi mantido, mas a identidade visual foi completamente refeita com a nova paleta de cores e uma ilustração temática. O fluxo de recuperação de senha foi simplificado em relação ao protótipo, que pedia um "código" em vez de enviar um link direto, que é uma abordagem mais moderna e segura.
    *   **Por que mudou:** A mudança cria um impacto visual imediato, estabelece a nova marca e torna a experiência de entrada no sistema mais agradável. A simplificação do fluxo de recuperação de senha melhora a usabilidade. O processo de cadastro foi avaliado como "eficiente" por **87,5%** dos usuários no formulário de feedback.

*   **Formulários (Cadastro de Usuário e de Pet):**
    *   **O que mudou:** Os formulários foram redesenhados para maior clareza. As "tags" clicáveis do protótipo para as características do pet foram substituídas por **checkboxes**. Foi adicionada a indicação explícita de campos obrigatórios (`*Obrigatório`).
    *   **Por que mudou:** A troca para checkboxes melhora a acessibilidade e a usabilidade, pois é um padrão de interação universal. Embora uma protetora na validação tenha questionado a quantidade de dados, a maioria dos adotantes (87,5%) considerou que "a plataforma oferece informações suficientes", validando a decisão de manter os campos detalhados para garantir que o adotante tenha segurança e clareza, reduzindo contatos desnecessários para o protetor.

*   **Página de Listagem e Detalhes do Pet:**
    *   **O que mudou:** Os cards dos pets foram redesenhados para incluir mais informações visuais rápidas (ícones de gênero/espécie, localização, breve descrição). A página de detalhes foi reestruturada em seções claras (Informações, Contatos, Personalidade, História), diferente do layout de coluna única do protótipo.
    *   **Por que mudou:** A mudança foi validada pelo feedback: **87,5%** dos usuários concordaram que as informações sobre os animais estão "bem organizadas e acessíveis". O novo layout permite que o usuário absorva os dados importantes rapidamente.

*   **Página de Perfil do Usuário:**
    *   **O que mudou:** O perfil no protótipo era mais simples. A versão final apresenta um layout mais limpo, com destaque para as ações principais ("Cadastrar novo animal") e métricas ("Animais divulgados", "Animais adotados"). Adicionamos os botões "Editar" e "Remover" aos cards dos pets do próprio usuário.
    *   **Por que mudou:** O novo design foca nas ações que o protetor mais precisa realizar, melhorando a eficiência do gerenciamento de seus anúncios.

---

## 3. Mudanças e Adições de Funcionalidade

A implementação não apenas seguiu o plano, mas também incorporou novas funcionalidades que surgiram da maturação do projeto e, principalmente, do feedback direto dos usuários.

*   **Funcionalidade Adicionada: Sistema de Depoimentos (Página Completa)**
    *   **O que mudou:** O protótipo não possuía esta funcionalidade. Foi criada uma página dedicada onde os usuários podem criar, editar e deletar seus próprios depoimentos.
    *   **Por que mudou:** A adição foi uma decisão estratégica para criar "prova social". A validação confirmou sua importância: **75%** dos usuários sentiram que a plataforma transmite "confiança e segurança", e os depoimentos são um fator chave para isso. Durante a validação, surgiu a sugestão de evoluir para um sistema de "estrelas ou curtidas", que foi registrada como uma melhoria para o futuro.

*   **Funcionalidade Adicionada: Páginas Institucionais (App `sobre_nos`)**
    *   **O que mudou:** O protótipo focava nas telas interativas. Foram adicionadas as páginas "Quem Somos", "Termos de Serviço" e "Política de Privacidade".
    *   **Por que mudou:** São páginas essenciais para garantir a transparência, credibilidade e conformidade legal de qualquer aplicação web, transmitindo mais profissionalismo ao projeto.

*   **Funcionalidade Modificada: Fluxo de Autenticação Completo**
    *   **O que mudou:** O fluxo de autenticação foi implementado com **confirmação de cadastro por e-mail** e um fluxo completo de **recuperação de senha** via link.
    *   **Por que mudou:** Embora não detalhadas visualmente no protótipo, estas são funcionalidades cruciais para a segurança das contas dos usuários, um ponto valorizado por 75% dos respondentes na pesquisa de confiança.

*   **Funcionalidade Adicionada: Marcar Pet como "Adotado"**
    *   **O que mudou:** No protótipo, a gestão se resumia a editar/remover. Foi adicionada a função "Marcar como Adotado".
    *   **Por que mudou:** Esta é uma necessidade prática para protetores. Permite que eles mantenham um histórico de sucesso, contribui para as métricas da plataforma e informa claramente aos outros usuários que aquele pet já encontrou um lar, sem precisar apagar o registro.