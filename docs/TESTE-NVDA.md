# Teste com NVDA

Status: PENDENTE DE CONFIRMAÇÃO DA LEITURA. Não registrar esta etapa como aprovada.

Foi baixado o NVDA 2026.3 do site oficial. A assinatura digital foi verificada como válida, com publicador NV Access Limited. Foi preparada uma cópia portátil em `tmp/`, ignorada pelo Git. O programa inicializou, mas a automação de janelas não conseguiu concluir a interação com a tela de boas-vindas. A abertura do programa não comprova o teste da livraria.

## Roteiro individual

1. Iniciar o projeto (`npm run dev -- --port 5174 --strictPort`) e abrir http://127.0.0.1:5174/ no Chrome.
2. Iniciar o NVDA e fechar as boas-vindas. Opcionalmente abrir NVDA → Ferramentas → Visualizador de fala para acompanhar os anúncios.
3. Recarregar a página. Conferir idioma, título do documento, um título de nível 1 e os títulos dos livros; usar H para cabeçalhos e G para imagens, em modo de navegação.
4. Usar Tab e Shift+Tab. Conferir o link Pular para o conteúdo, a ordem de foco e o foco visível.
5. Adicionar Book 1 com Enter e Book 2 com Espaço. Ouvir o nome específico do botão e a mensagem de adição e total.
6. Abrir Carrinho pelo link. Conferir o título da página, a leitura de Seu carrinho e as quantidades.
7. Remover um título e depois o último. Conferir os anúncios de remoção, o total e o foco no título principal.
8. Usar Continuar escolhendo livros e confirmar retorno ao catálogo sem armadilha de teclado.
9. Registrar data, versões, resultado observado e problemas. Capturar uma tela real do Visualizador de fala, sem dados de outros aplicativos. Corrigir problemas e repetir os passos afetados.

Os resultados esperados acima são critérios de teste, não resultados observados.
