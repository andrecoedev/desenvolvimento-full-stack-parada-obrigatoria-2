"""Gera o PDF da atividade de acessibilidade da livraria."""
import json
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output' / 'pdf'
OUT.mkdir(parents=True, exist_ok=True)
FILE = OUT / 'AndreLucasCoelhoDeJesus_ProjetoLivrariaOnline_Acessibilidade.pdf'
REPO = 'https://github.com/andrecoedev/desenvolvimento-full-stack-parada-obrigatoria-2'
for name, filename in [('Arial', 'arial.ttf'), ('Arial-Bold', 'arialbd.ttf')]:
    pdfmetrics.registerFont(TTFont(name, 'C:/Windows/Fonts/' + filename))
pdfmetrics.registerFontFamily('Arial', normal='Arial', bold='Arial-Bold', italic='Arial', boldItalic='Arial-Bold')
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Body', fontName='Arial', fontSize=10, leading=15, spaceAfter=9, textColor=colors.HexColor('#253732')))
styles.add(ParagraphStyle(name='SmallText', parent=styles['Body'], fontSize=8, leading=11, spaceAfter=7))
styles.add(ParagraphStyle(name='CaptionText', parent=styles['SmallText'], textColor=colors.HexColor('#52645c'), spaceBefore=5))
styles.add(ParagraphStyle(name='PageTitle', fontName='Arial-Bold', fontSize=22, leading=27, spaceAfter=16, textColor=colors.HexColor('#174f42')))
styles.add(ParagraphStyle(name='SectionTitle', fontName='Arial-Bold', fontSize=13, leading=18, spaceBefore=10, spaceAfter=7, textColor=colors.HexColor('#174f42')))
story = []

def p(text, style='Body'):
    return Paragraph(text, styles[style])

def add(text, style='Body'):
    story.append(p(text, style))

def title(text):
    add(text, 'PageTitle')

def section(text):
    add(text, 'SectionTitle')

def shot(name, caption, max_height=240):
    image = Image(str(ROOT / 'evidencias' / name))
    ratio = min(499 / image.imageWidth, max_height / image.imageHeight)
    image.drawWidth = image.imageWidth * ratio
    image.drawHeight = image.imageHeight * ratio
    image.hAlign = 'LEFT'
    story.extend([image, p(caption, 'CaptionText'), Spacer(1, 6)])

def table(rows, widths):
    cells = [[p(escape(str(cell)), 'SmallText') for cell in row] for row in rows]
    t = Table(cells, colWidths=widths, hAlign='LEFT', repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e4eee8')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LINEBELOW', (0, 0), (-1, -1), 0.4, colors.HexColor('#c4cec8')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 4)
    ]))
    story.extend([t, Spacer(1, 8)])

audits = {}
for key in ['antes-catalogo', 'antes-carrinho', 'depois-catalogo', 'depois-carrinho']:
    audits[key] = json.loads((ROOT / 'evidencias' / (key + '.report.json')).read_text(encoding='utf-8'))
score = lambda key: round(audits[key]['categories']['accessibility']['score'] * 100)
keyboard = json.loads((ROOT / 'evidencias' / 'testes-teclado.json').read_text(encoding='utf-8'))
nvda_file = ROOT / 'evidencias' / 'resultado-nvda.json'
nvda = json.loads(nvda_file.read_text(encoding='utf-8')) if nvda_file.exists() else None

title('Livraria online: acessibilidade')
add('Desenvolvimento Full Stack<br/><b>Parada Obrigatória 2 - SENAI</b>', 'SectionTitle')
add('<b>Aluno:</b> André Lucas Coelho de Jesus<br/><b>Data:</b> 7 de novembro de 2026<br/><b>Prazo no enunciado:</b> 9 de novembro de 2026, às 23h59')
section('1. Descrição do projeto')
add('Esta atividade usa uma livraria simples, com dois livros no catálogo. É possível adicionar mais de um exemplar ao carrinho e depois remover os títulos escolhidos. A aplicação usa React na interface, Redux para guardar os itens e React Router para navegar entre o catálogo e o carrinho. Não há cadastro ou pagamento. Ao recarregar a página, o carrinho fica vazio, pois os dados são guardados apenas na memória.')
section('2. Desenvolvimento da atividade')
add('A base foi o exemplo do enunciado. Para executá-lo com as versões instaladas, foi necessário atualizar a inicialização do React e a forma de declarar as rotas. As regras do carrinho continuaram iguais. Uma cópia dessa primeira versão ficou na pasta baseline para permitir a comparação com o resultado final.')
add('O catálogo passou pela primeira auditoria antes das mudanças. O carrinho inicial foi avaliado depois, usando a cópia preservada. Nas duas páginas, o Lighthouse 13.6.0 foi executado no Chrome, sem janela visível, com a opção Accessibility e o perfil desktop. O teste de teclado usou o Playwright para acionar as teclas no navegador. A verificação com NVDA ficou separada desses testes.')
table([['Página auditada', 'Antes', 'Depois'], ['Catálogo', score('antes-catalogo'), score('depois-catalogo')], ['Carrinho vazio', score('antes-carrinho'), score('depois-carrinho')]], [299, 100, 100])
add('A nota do Lighthouse vai até 100 e considera as verificações automáticas aplicáveis à página. Mesmo com a nota máxima, o uso por teclado e a leitura com NVDA precisam ser conferidos. Essa nota não equivale a uma avaliação completa das WCAG.', 'SmallText')
section('Código e evidências')
add(f'<link href="{REPO}" color="#174f42"><u>Código da atividade no GitHub</u></link>')
add('Repositório: andrecoedev / desenvolvimento-full-stack-parada-obrigatoria-2. A pasta evidencias reúne os relatórios originais em HTML e JSON, as capturas da aplicação e o resultado do teste de teclado.', 'SmallText')
if not nvda:
    add('O código e as auditorias estão concluídos. Falta confirmar a leitura com NVDA e atualizar esse resultado antes de enviar o PDF ao AVA.', 'SmallText')
story.append(PageBreak())

title('3. Análise da aplicação inicial')
shot('antes-catalogo-detalhe.png', 'Figura 1. Catálogo antes das melhorias. Detalhe do canto superior esquerdo da base preservada. A captura completa está no repositório.', 220)
shot('antes-carrinho-detalhe.png', 'Figura 2. Carrinho vazio antes das melhorias, na mesma região da tela.', 120)
section('Problemas identificados')
add('Na versão inicial, o Lighthouse apontou a falta do idioma no elemento html e da região principal da página. Esses problemas aparecem no relatório como html-has-lang e landmark-one-main. A nota foi 84 no catálogo e 79 no carrinho vazio. Embora os problemas fossem os mesmos, as páginas tinham conjuntos diferentes de verificações aplicáveis.')
add('O código também mostrava dificuldades que a nota não explicava sozinha. A lista começava diretamente com os títulos dos livros em h2, sem um h1 para apresentar a página. Não havia um link para abrir o carrinho. Além disso, os dois botões se chamavam apenas "Add to Cart": fora do contexto visual, o nome não dizia qual livro seria adicionado. As mudanças no carrinho não tinham uma região de aviso para leitores de tela.')
add('Os botões já eram elementos HTML nativos e podiam ser acionados pelo teclado. A versão inicial não tinha imagens, por isso não havia atributos alt a corrigir. A análise inicial não registrou falhas de contraste.', 'SmallText')
story.append(PageBreak())

title('4. Melhorias de acessibilidade')
shot('depois-catalogo.png', 'Figura 3. Catálogo após as melhorias, com navegação, títulos e capas ilustrativas.', 280)
add('A primeira mudança foi organizar a página: um título principal, uma área de conteúdo e links para o catálogo e o carrinho. Os nomes dos botões passaram a incluir o livro. Assim, "Adicionar ao carrinho: Book 1" identifica a ação mesmo quando o botão é encontrado isoladamente pelo leitor de tela.', 'SmallText')
table([
    ['Alteração', 'Benefício e critérios WCAG relacionados'],
    ['Idioma pt-BR e título de cada página', 'Define o idioma de leitura e identifica a página aberta (3.1.1; 2.4.2).'],
    ['Regiões HTML, listas, h1 e h2', 'Organiza o conteúdo para navegação por regiões e cabeçalhos (1.3.1; 2.4.6).'],
    ['Capas ilustrativas com texto alternativo', 'Descreve as imagens acrescentadas ao catálogo (1.1.1).'],
    ['Links, foco visível e atalho ao conteúdo', 'Permite usar a interface sem mouse e acompanhar a posição do foco (2.1.1; 2.4.1; 2.4.7).'],
    ['Nome dos botões com o livro', 'Mantém o texto visível completo e identifica o título da ação (2.5.3; 4.1.2).'],
    ['Avisos e ajuste do foco', 'Informa mudanças no carrinho e orienta após navegar ou remover um item (4.1.3; 2.4.3).'],
    ['Contraste e adaptação à largura', 'Facilita a leitura e o uso em telas estreitas (1.4.3; 1.4.10).']
], [175, 324])
add('Os botões e links continuam sendo elementos nativos do HTML, que já respondem ao teclado. O tabindex=-1 foi usado nos títulos e no conteúdo para receber foco pelo código, sem criar paradas extras no Tab. As capas foram acrescentadas para demonstrar o texto alternativo, já que o exemplo inicial não tinha imagens.', 'SmallText')
story.append(PageBreak())

title('5. Carrinho e navegação')
shot('depois-carrinho-preenchido.png', 'Figura 4. Carrinho com dois títulos e três exemplares. Foco no título após navegar.', 260)
shot('depois-carrinho-vazio.png', 'Figura 5. Carrinho após remover o último título. O foco retorna ao h1.', 220)
add('No exemplo acima, Book 1 aparece com quantidade 2 e Book 2 com quantidade 1. Ao remover Book 1, suas duas cópias saem juntas, como já acontecia no código base. A diferença é que agora a quantidade fica visível e o nome acessível do botão explica que a remoção vale para todas as cópias daquele título.')
add('A remoção também exigiu cuidado com o foco. Como o botão some junto com o livro, o foco volta ao título "Seu carrinho". Ao trocar de página, a aplicação atualiza o título da aba e leva o foco ao h1. Os avisos de adição e remoção ficam em uma região com role=status, aria-live=polite e aria-atomic=true.')
story.append(PageBreak())

title('6. Auditorias antes e depois')
shot('antes-catalogo-lighthouse.png', 'Figura 6. Relatório inicial do catálogo: 84/100. O arquivo original HTML/JSON está no GitHub.', 250)
shot('depois-catalogo-lighthouse.png', 'Figura 7. Relatório final do catálogo: 100/100. Os itens de verificação manual continuam indicados pela ferramenta.', 250)
add('No carrinho vazio, a nota passou de 79/100 para 100/100. Os relatórios e as capturas dessa página estão na pasta evidencias. O teste de teclado cobriu o carrinho preenchido. A auditoria padrão do Lighthouse recarrega a página, o que esvazia os itens guardados na memória.')
add('Houve um ajuste mesmo depois de alcançar a nota 100. O Lighthouse ainda mostrava um aviso porque o nome acessível do botão interrompia a expressão "Adicionar ao carrinho" com o nome do livro. O rótulo foi alterado para "Adicionar ao carrinho: Book 1", mantendo o texto visível completo no início. Na nova auditoria do catálogo, esse aviso deixou de aparecer.', 'SmallText')
story.append(PageBreak())

title('7. Testes realizados')
section('Teclado e comportamento')
add('O teste começou pelo link "Pular para o conteúdo". Tab colocou o foco no link e Enter levou ao conteúdo principal. Nos botões dos livros, Enter e Espaço adicionaram exemplares e atualizaram o texto de status. Depois, Shift+Tab permitiu voltar ao link do carrinho. Ao abri-lo, o título da aba mudou e o foco ficou no h1.')
add('No carrinho, Espaço removeu as duas cópias de Book 1 e manteve Book 2. O foco voltou ao título principal. Após remover o último livro, apareceu a mensagem de carrinho vazio. O link "Continuar escolhendo livros" também funcionou com Enter e devolveu o foco ao título do catálogo.')
add('As sete verificações automatizadas passaram. O fluxo não registrou erros de JavaScript. Nas larguras de 320 e 640 pixels CSS, a página não apresentou rolagem horizontal. Essa verificação de largura não substitui um teste de zoom real.', 'SmallText')
add('Os três testes do Redux também passaram. Eles conferem a adição de cópias sem modificar o estado anterior, a remoção de todas as cópias de um título preservando os demais e a remoção do último livro. Uma ação desconhecida manteve o estado como estava. A versão de produção foi gerada sem falha (build).', 'SmallText')
section('Verificação com NVDA')
if nvda:
    add(escape(nvda['summary']))
    add('Registro fornecido pelo aluno: ' + escape(nvda['observations']), 'SmallText')
else:
    add('O teste com NVDA continua pendente. A versão 2026.3 foi baixada do site oficial, teve a assinatura de NV Access Limited conferida e abriu em modo portátil. A primeira tentativa parou na janela de boas-vindas. Na segunda, o controle automático do Chrome foi interrompido porque a ferramenta não conseguiu verificar o endereço aberto com segurança. Por isso, ainda falta confirmar a leitura dos botões e dos avisos do carrinho.')
    add('A próxima etapa é usar a livraria no Chrome com o NVDA ativo e registrar o que ele anuncia ao navegar pelos títulos e capas, adicionar livros e remover os itens. O roteiro está em docs/TESTE-NVDA.md. O Visualizador de fala pode ajudar a guardar esse registro.', 'SmallText')
section('Limites dos resultados')
add('O catálogo e o carrinho passaram nas auditorias finais, e o fluxo de teclado conseguiu completar as ações previstas. Falta conferir se o NVDA anuncia os avisos de status. Também não foram realizados teste de zoom real, avaliação com usuários com deficiência ou revisão de todos os critérios WCAG 2.2. Essas etapas limitam o que se pode concluir sobre a acessibilidade da aplicação.')
section('Referências consultadas')
for label, url in [
    ('W3C - Referência rápida WCAG 2.2', 'https://www.w3.org/WAI/WCAG22/quickref/'),
    ('Chrome Developers - Pontuação de acessibilidade Lighthouse', 'https://developer.chrome.com/docs/lighthouse/accessibility/scoring'),
    ('NV Access - Download oficial do NVDA', 'https://www.nvaccess.org/download/'),
    ('NVDA - Manual do usuário', 'https://download.nvaccess.org/documentation/userGuide.html'),
    ('React - createRoot', 'https://react.dev/reference/react-dom/client/createRoot'),
    ('React Router - Rotas declarativas', 'https://reactrouter.com/start/declarative/routing')
]:
    add(f'<link href="{url}" color="#174f42"><u>{label}</u></link>', 'SmallText')

def page_frame(c, doc):
    c.setStrokeColor(colors.HexColor('#c4cec8'))
    c.line(48, 43, A4[0]-48, 43)
    c.setFont('Arial', 8)
    c.setFillColor(colors.HexColor('#52645c'))
    c.drawString(48, 29, 'SENAI | Livraria online - Acessibilidade | 07/11/2026')
    c.drawRightString(A4[0]-48, 29, f'Página {doc.page}')

doc = SimpleDocTemplate(str(FILE), pagesize=A4, rightMargin=48, leftMargin=48, topMargin=43, bottomMargin=58,
                        title='Projeto Livraria Online - Acessibilidade', author='André Lucas Coelho de Jesus')
doc.build(story, onFirstPage=page_frame, onLaterPages=page_frame)
print(FILE)
