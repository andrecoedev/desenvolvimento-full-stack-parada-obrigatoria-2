# Desenvolvimento Full Stack - Parada Obrigatória 2

Projeto acadêmico do SENAI: melhorias de acessibilidade em uma livraria com React, Redux e React Router.

## Executar

Requisitos: Node.js 22.12 ou superior compatível com o Vite instalado e npm.

```sh
npm ci
npm run dev
```

Abra o endereço mostrado no terminal. O catálogo fica em `/` e o carrinho em `/cart`.

```sh
npm test
npm run build
npm run preview
```

Não há backend, pagamento, conta de usuário ou armazenamento permanente. Recarregar a página esvazia o carrinho.

## Organização

- `src/App.jsx`: rotas, navegação, título do documento e região de avisos.
- `src/components/`: catálogo e carrinho.
- `src/store.js`: ações Redux para adicionar e remover livros.
- `src/style.css`: estilos, foco visível e adaptação à largura da tela.
- `public/capas/`: duas capas SVG ilustrativas criadas para a demonstração.
- `baseline/`: cópia da base antes das melhorias.
- `evidencias/`: relatórios originais Lighthouse, capturas reais e resultados dos testes.
- `docs/`: análise e roteiro de verificação com NVDA.
- `output/pdf/`: relatório da atividade.

## Base do enunciado

A lógica e os dois títulos (`Book 1` e `Book 2`) vieram do exemplo fornecido. Para executar com as versões instaladas, `ReactDOM.render` foi substituído por `createRoot`, e `Switch` por `Routes`, usando `element` nas rotas. Essas adaptações já estavam presentes na auditoria inicial. O HTML inicial tinha apenas charset, viewport, título e o ponto de montagem; não foram acrescentados problemas artificiais de contraste, botões ou imagens à base.

Para abrir a base preservada em um terminal separado:

```sh
npx vite baseline --host 127.0.0.1 --port 5175
```

Acesse `http://127.0.0.1:5175/` e `http://127.0.0.1:5175/cart`. A base não tem links entre as páginas, como no enunciado. Remover um título elimina todas as suas cópias; a versão melhorada preserva essa regra, agrupa os títulos e exibe a quantidade.

## Acessibilidade

Idioma `pt-BR`, regiões semânticas, um `h1` por página, listas de livros, texto alternativo nas capas, links de navegação, nomes de botões específicos, foco visível, atalho para o conteúdo, foco após troca de rota e remoção, e avisos em `role="status"` com `aria-live="polite"`.

As capas não existiam no exemplo original: foram adicionadas na versão melhorada para demonstrar `alt`. Os botões originais já eram controles nativos operáveis por teclado; não foi necessário adicionar `tabindex="0"`. ARIA complementa a semântica nativa, sem substituí-la.

## Resultados reais em 07/11/2026

Lighthouse 13.6.0, Chrome, preset desktop, categoria Accessibility, navegação local:

| Página | Antes | Depois |
| --- | ---: | ---: |
| Catálogo | 84 | 100 |
| Carrinho vazio | 79 | 100 |

Os testes automatizados de teclado foram executados em Chrome via Playwright, sem NVDA. Foram conferidos Tab, Shift+Tab, Enter, Espaço, rotas, foco, duplicação e remoção de livros, além de larguras de 320 e 640 CSS pixels. Os três testes do reducer passaram. Veja `evidencias/testes-teclado.json` para os detalhes. Os testes de navegador usam a porta 5174; inicie com `npm run dev -- --port 5174 --strictPort` e execute `node scripts/testar-navegador.mjs`.

Uma nota 100 não demonstra conformidade integral com WCAG e não substitui teclado e leitor de tela. A navegação Lighthouse no carrinho foi feita com o estado vazio; o estado preenchido foi verificado no fluxo de teclado. A situação do teste NVDA está em `docs/TESTE-NVDA.md`.

Para repetir uma auditoria (Chrome instalado):

```sh
npx lighthouse http://127.0.0.1:5174/ --only-categories=accessibility --preset=desktop --chrome-flags="--headless=new" --output=html --output=json --output-path=./evidencias/depois-catalogo
```

O build passou. O Vite exibe avisos sobre a diretiva `use client` dos arquivos do React Router; esta aplicação usa renderização no navegador e não usa React Server Components.

## Entrega

Código na branch `dev`: https://github.com/andrecoedev/desenvolvimento-full-stack-parada-obrigatoria-2/tree/dev

Revisar o PDF e concluir a validação individual com NVDA antes do envio pelo aluno ao AVA. Prazo do enunciado: 09/11/2026, às 23h59.

## Referências

- WCAG 2.2: https://www.w3.org/WAI/WCAG22/quickref/
- Pontuação do Lighthouse: https://developer.chrome.com/docs/lighthouse/accessibility/scoring
- NVDA e manual: https://www.nvaccess.org/download/ e https://download.nvaccess.org/documentation/userGuide.html
- React: https://react.dev/reference/react-dom/client/createRoot
- React Router: https://reactrouter.com/start/declarative/routing
