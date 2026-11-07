# Análise da acessibilidade

Data: 07/11/2026. Base: exemplo da atividade Desenvolvimento Full Stack - Parada Obrigatória 2, SENAI.

## Antes

Lighthouse 13.6.0, Chrome real em modo headless, desktop, categoria Accessibility. Catálogo: 84/100; carrinho vazio: 79/100. Os relatórios HTML e JSON estão em `evidencias/`. As duas falhas automáticas foram `html-has-lang` (sem idioma no elemento html) e `landmark-one-main` (sem região principal). As notas diferem porque as verificações aplicáveis às páginas não são idênticas.

A inspeção encontrou também ausência de `h1`, botões repetidos com nomes genéricos, ausência de navegação entre páginas e de anúncio para alterações do carrinho. Os botões nativos já funcionavam com teclado. A base não continha imagens, logo não houve falha inicial de `alt` a corrigir. Não foi afirmado que existia falha de contraste na base.

## Melhorias e relação com WCAG 2.2

| Alteração | Benefício | Critérios relacionados |
| --- | --- | --- |
| `lang="pt-BR"` | Define o idioma de leitura | 3.1.1 |
| `header`, `nav`, `main`, `footer`, listas, h1 e h2 | Estrutura e navegação por regiões e cabeçalhos | 1.3.1, 2.4.1, 2.4.6 |
| Capas ilustrativas com alt descritivo | Disponibiliza alternativa textual ao conteúdo visual novo | 1.1.1 |
| Links e botões nativos, ordem natural de foco | Operação sem mouse | 2.1.1, 2.1.2, 2.4.3 |
| Foco visível e link para pular ao conteúdo | Localização do foco e redução de repetição | 2.4.1, 2.4.7 |
| Nome acessível inclui texto visível e título do livro | Diferencia ações e preserva identificação por voz | 2.5.3, 4.1.2 |
| `role="status"`, aria-live e aria-atomic | Comunica mudanças sem mover o foco | 4.1.3 |
| Título de documento por rota e foco no h1 | Orienta na troca de página e após remoções | 2.4.2, 2.4.3 |
| Texto escuro sobre fundo claro e layout flexível | Legibilidade e adaptação a telas estreitas | 1.4.3, 1.4.10 |

Essa associação explica as escolhas; não é certificação de conformidade integral com todos os critérios WCAG.

## Verificações finais

Lighthouse: catálogo 100/100, carrinho vazio 100/100. Durante a implementação, houve um aviso de `label-content-name-mismatch`, embora a pontuação fosse 100. Os nomes dos botões foram corrigidos para começar pelo texto visível completo e a auditoria do catálogo foi repetida sem esse aviso.

Testes automatizados: três casos do reducer; fluxo com Tab, Shift+Tab, Enter e Espaço; foco após rotas e remoção; avisos dinâmicos presentes no DOM; carrinho com cópias, com um título e vazio; retorno ao catálogo; ausência de erro JavaScript; ausência de rolagem horizontal em 320 e 640 CSS pixels.

O teste de DOM da região de status não prova que um leitor de tela anunciou o texto. A verificação com NVDA é registrada separadamente. Não foi feito teste de zoom real nem avaliação com usuários com deficiência.
