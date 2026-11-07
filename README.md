# Livraria online - Acessibilidade

**Aluno:** André Lucas Coelho de Jesus

**Disciplina:** Desenvolvimento Full Stack - SENAI

**Atividade:** Parada Obrigatória 2

## Sobre a atividade

O projeto usa a livraria do enunciado como ponto de partida para trabalhar acessibilidade. A aplicação tem uma lista de livros e um carrinho, usando React, Redux e React Router.

As mudanças incluem títulos organizados, descrição das capas, links entre as páginas, foco visível e avisos ao adicionar ou remover livros. O carrinho guarda os itens apenas enquanto a página está aberta; ao recarregar, ele fica vazio.

## Como executar

É necessário ter Node.js 22.12 ou uma versão mais recente compatível com o Vite, além do npm.

```sh
npm install
npm run dev
```

Depois, abra o endereço mostrado no terminal. A página inicial exibe os livros, e o link Carrinho abre os itens adicionados.

## Avaliação de acessibilidade

Auditorias com Lighthouse 13.6.0 no Chrome, usando a categoria Accessibility e o perfil desktop, em 07/11/2026:

| Página | Antes | Depois |
| --- | ---: | ---: |
| Catálogo | 84 | 100 |
| Carrinho vazio | 79 | 100 |

O fluxo de teclado foi verificado com testes automatizados no Chrome. Os testes do carrinho e a geração da versão de produção também passaram. A leitura com NVDA ainda precisa ser concluída. A nota do Lighthouse não substitui essa verificação.

## Arquivos da entrega

- `src/`: código da livraria.
- `baseline/`: versão anterior às melhorias.
- `evidencias/`: capturas, relatórios Lighthouse e resultados dos testes.
- `docs/`: análise dos problemas e roteiro para o NVDA.
- `output/pdf/`: relatório da atividade.

As duas capas são ilustrativas e foram acrescentadas para demonstrar o uso de texto alternativo. O exemplo original não tinha imagens.
