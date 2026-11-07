"""Gera o relatório com evidências existentes, sem fabricar resultados."""
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
REPO = 'https://github.com/andrecoedev/desenvolvimento-full-stack-parada-obrigatoria-2/tree/dev'
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
add('A livraria tem um catálogo com dois livros e um carrinho de compras. O usuário pode adicionar exemplares e remover os títulos escolhidos. A interface usa React, o Redux guarda os itens do carrinho e o React Router permite navegar entre as páginas. Por ser um projeto acadêmico, a aplicação não tem cadastro nem pagamento. Os itens ficam na memória e são apagados quando a página é recarregada.')
section('2. Método e escopo')
add('O projeto partiu do código fornecido no enunciado. Antes da primeira auditoria, a inicialização do React e as rotas foram ajustadas às versões instaladas. A lógica dos livros e do carrinho foi mantida. A pasta baseline guarda essa versão, anterior às melhorias de acessibilidade.')
add('A primeira auditoria do catálogo ocorreu antes das alterações. A avaliação do carrinho inicial usou a cópia preservada, em uma execução posterior. Nas duas páginas, foi usado o Lighthouse 13.6.0, com a categoria Accessibility e o perfil desktop, no Chrome em modo headless (sem janela visível). O Playwright executou o fluxo de teclado no Chrome. A leitura com NVDA tem um registro próprio, pois o teste de teclado não confirma o que o leitor de tela anuncia.')
table([['Página auditada', 'Antes', 'Depois'], ['Catálogo', score('antes-catalogo'), score('depois-catalogo')], ['Carrinho vazio', score('antes-carrinho'), score('depois-carrinho')]], [299, 100, 100])
add('As notas vão de 0 a 100. A nota máxima indica que a página passou nas verificações automáticas aplicáveis. Ainda é necessário conferir teclado e leitor de tela para avaliar aspectos que o Lighthouse não testa. O resultado, sozinho, não comprova conformidade integral com WCAG.', 'SmallText')
section('Código e evidências')
add(f'<link href="{REPO}" color="#174f42"><u>Abrir o repositório no GitHub - branch dev</u></link>')
add('Repositório: andrecoedev / desenvolvimento-full-stack-parada-obrigatoria-2. A pasta evidencias reúne os relatórios originais em HTML e JSON, as capturas da aplicação e o resultado do teste de teclado.', 'SmallText')
if not nvda:
    add('O código e as auditorias estão concluídos. Falta confirmar a leitura com NVDA e atualizar esse resultado antes de enviar o PDF ao AVA.', 'SmallText')
story.append(PageBreak())

title('3. Análise da aplicação inicial')
shot('antes-catalogo-detalhe.png', 'Figura 1. Catálogo antes das melhorias. Detalhe do canto superior esquerdo da base preservada. A captura completa está no repositório.', 220)
shot('antes-carrinho-detalhe.png', 'Figura 2. Carrinho vazio antes das melhorias, na mesma região da tela.', 120)
section('Problemas identificados')
add('O Lighthouse encontrou dois problemas nas duas páginas: faltava definir o idioma no elemento html (html-has-lang) e indicar a região principal do conteúdo (landmark-one-main). O catálogo recebeu 84/100 e o carrinho vazio, 79/100. As notas são diferentes porque cada página tem seu conjunto de verificações aplicáveis.')
add('A leitura do código mostrou outras limitações. As páginas começavam com h2, sem um h1, e não havia links entre o catálogo e o carrinho. Os botões tinham nomes genéricos, sem informar a qual livro se referiam. Adicionar ou remover itens também não produzia um aviso para leitores de tela.')
add('Os botões já eram elementos HTML nativos e podiam ser acionados pelo teclado. A versão inicial não tinha imagens, por isso não havia atributos alt a corrigir. A análise inicial não registrou falhas de contraste.', 'SmallText')
story.append(PageBreak())

title('4. Melhorias de acessibilidade')
shot('depois-catalogo.png', 'Figura 3. Catálogo após as melhorias, com navegação, títulos e capas ilustrativas.', 280)
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
add('Os links e botões usam os controles nativos do HTML. O tabindex=-1 permite que o código leve o foco ao conteúdo e aos títulos, sem incluir essas regiões na sequência do Tab. Os atributos ARIA complementam os nomes dos botões e os avisos do carrinho.', 'SmallText')
story.append(PageBreak())

title('5. Carrinho e navegação')
shot('depois-carrinho-preenchido.png', 'Figura 4. Carrinho com dois títulos e três exemplares. Foco no título após navegar.', 260)
shot('depois-carrinho-vazio.png', 'Figura 5. Carrinho após remover o último título. O foco retorna ao h1.', 220)
add('A remoção segue a regra do código base: retirar um título apaga todas as cópias desse livro. Agora, o carrinho reúne as cópias em uma linha e mostra a quantidade. O nome acessível do botão informa que todas elas serão removidas.')
add('Quando o usuário abre outra página, a aplicação atualiza o título do documento e leva o foco ao h1. Depois de uma remoção, o foco volta ao título do carrinho, pois o botão acionado deixa de existir. Uma região com role=status, aria-live=polite e aria-atomic=true recebe os avisos de adição e remoção.')
story.append(PageBreak())

title('6. Auditorias antes e depois')
shot('antes-catalogo-lighthouse.png', 'Figura 6. Relatório inicial do catálogo: 84/100. O arquivo original HTML/JSON está no GitHub.', 250)
shot('depois-catalogo-lighthouse.png', 'Figura 7. Relatório final do catálogo: 100/100. Os itens de verificação manual continuam indicados pela ferramenta.', 250)
add('No carrinho vazio, a nota passou de 79/100 para 100/100. Os relatórios e as capturas dessa página estão na pasta evidencias. O teste de teclado cobriu o carrinho preenchido. A auditoria padrão do Lighthouse recarrega a página, o que esvazia os itens guardados na memória.')
add('Uma das auditorias trouxe um aviso sobre a diferença entre o texto visível e o nome acessível dos botões, mesmo com nota 100. Após o ajuste, o nome passou a começar pelo texto visível completo. A nova auditoria do catálogo não apresentou esse aviso.', 'SmallText')
story.append(PageBreak())

title('7. Testes realizados')
section('Teclado e comportamento')
for result in keyboard['results']:
    add(f'{escape(result["name"])}: {escape(result["detail"])}', 'SmallText')
add('O fluxo automatizado com teclas simuladas no Chrome passou nas sete verificações. Também passaram os três testes do Redux, que cobrem a adição de cópias sem alterar o estado anterior, a remoção de todas as cópias de um título sem afetar os demais e a remoção do último livro. As ações desconhecidas preservaram o estado. A geração da versão de produção (build) foi concluída.')
section('Verificação com NVDA')
if nvda:
    add(escape(nvda['summary']))
    add('Registro fornecido pelo aluno: ' + escape(nvda['observations']), 'SmallText')
else:
    add('O teste com NVDA continua pendente. A versão 2026.3 foi obtida no site oficial, teve a assinatura de NV Access Limited verificada e iniciou em cópia portátil. Na primeira tentativa, houve uma falha ao controlar a janela de boas-vindas. Na nova tentativa, o programa iniciou, mas a ferramenta de automação interrompeu o controle do Chrome por não conseguir verificar o endereço da página com segurança. Os anúncios da livraria ainda não foram confirmados.')
    add('Para concluir, é preciso percorrer a livraria no Chrome com o NVDA ativo, conferir os títulos e as capas e usar Tab, Shift+Tab, Enter e Espaço nas ações do carrinho. O registro deve informar os nomes e avisos lidos ao adicionar livros, abrir o carrinho e remover os itens. O arquivo docs/TESTE-NVDA.md contém o roteiro, incluindo o uso opcional do Visualizador de fala para guardar a evidência.', 'SmallText')
section('Limites dos resultados')
add('As auditorias e o teste de teclado confirmaram as melhorias descritas na estrutura e no uso do carrinho. A leitura dos avisos de status depende da verificação com NVDA: a presença do texto na página não confirma seu anúncio. Também ficaram fora desta avaliação o zoom real, os testes com usuários com deficiência e a revisão de todos os critérios WCAG 2.2. Portanto, os resultados se limitam às verificações registradas neste relatório.')
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
