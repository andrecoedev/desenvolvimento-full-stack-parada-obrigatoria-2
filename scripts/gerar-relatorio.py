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
add('A aplicação permite consultar dois livros, adicioná-los ao carrinho e remover os títulos selecionados. Foi desenvolvida em React, com Redux para o estado do carrinho e React Router para as páginas de catálogo e carrinho. É uma demonstração acadêmica, sem pagamento ou cadastro. O carrinho fica apenas na memória e é esvaziado ao recarregar a página.')
section('2. Método e escopo')
add('O ponto de partida foi o código fornecido no enunciado. A inicialização do React e a sintaxe das rotas foram adaptadas às versões instaladas antes da auditoria inicial, sem acrescentar falhas artificiais. A cópia anterior às melhorias está preservada na pasta baseline do repositório.')
add('O catálogo foi auditado antes das alterações. O carrinho inicial foi auditado posteriormente na cópia preservada. As verificações usaram Lighthouse 13.6.0, categoria Accessibility e preset desktop, no Chrome em modo headless. Os testes de teclado foram automatizados com Playwright no Chrome e são apresentados separadamente da verificação com NVDA.')
table([['Página auditada', 'Antes', 'Depois'], ['Catálogo', score('antes-catalogo'), score('depois-catalogo')], ['Carrinho vazio', score('antes-carrinho'), score('depois-carrinho')]], [299, 100, 100])
add('As notas são de 0 a 100. A pontuação 100 representa o resultado das verificações automáticas aplicáveis; não comprova conformidade integral com WCAG nem substitui testes com teclado e leitor de tela.', 'SmallText')
section('Código e evidências')
add(f'<link href="{REPO}" color="#174f42"><u>Abrir o repositório no GitHub - branch dev</u></link>')
add('Repositório: andrecoedev / desenvolvimento-full-stack-parada-obrigatoria-2. A pasta evidencias contém os relatórios originais HTML/JSON, capturas reais e o registro do fluxo de teclado.', 'SmallText')
if not nvda:
    add('<b>Situação da entrega:</b> código e auditorias concluídos; leitura com NVDA ainda pendente de confirmação. Este PDF deve ser revisado e atualizado antes do envio ao AVA.', 'SmallText')
story.append(PageBreak())

title('3. Análise da aplicação inicial')
shot('antes-catalogo-detalhe.png', 'Figura 1. Catálogo da base preservada. Captura real da região superior esquerda; o print completo também está no repositório.', 220)
shot('antes-carrinho-detalhe.png', 'Figura 2. Carrinho vazio da base preservada. Detalhe da região superior esquerda.', 120)
section('Problemas identificados')
add('<b>Lighthouse:</b> as duas páginas não tinham idioma definido no elemento html (html-has-lang) nem região principal (landmark-one-main). O catálogo obteve 84/100 e o carrinho vazio 79/100. As notas diferem porque as verificações aplicáveis não são idênticas.')
add('<b>Inspeção do código:</b> não havia h1, navegação entre catálogo e carrinho, identificação do livro nos nomes dos botões ou avisos para as alterações no carrinho. A ausência de links dificultava completar a compra simulada pela interface.')
add('Os botões originais já eram elementos nativos operáveis por teclado. A base não tinha imagens; portanto, não houve uma falha inicial de alt a corrigir. Também não foi alegado um problema de contraste inexistente na base.', 'SmallText')
story.append(PageBreak())

title('4. Melhorias de acessibilidade')
shot('depois-catalogo.png', 'Figura 3. Catálogo após as melhorias, com navegação, títulos e capas ilustrativas.', 280)
table([
    ['Alteração', 'Benefício e critérios WCAG relacionados'],
    ['Idioma pt-BR e títulos por rota', 'Orienta a leitura e identifica a página (3.1.1; 2.4.2).'],
    ['Regiões semânticas, listas, h1 e h2', 'Permite entender a estrutura e navegar por regiões e cabeçalhos (1.3.1; 2.4.6).'],
    ['Capas novas com texto alternativo', 'Fornece alternativa ao conteúdo visual incluído na demonstração (1.1.1).'],
    ['Links, foco visível e atalho ao conteúdo', 'Facilita a operação sem mouse e a localização do foco (2.1.1; 2.4.1; 2.4.7).'],
    ['Nome específico dos botões', 'Inclui o texto visível completo e o livro associado (2.5.3; 4.1.2).'],
    ['Região de status e foco gerenciado', 'Informa alterações e orienta após troca de página ou remoção (4.1.3; 2.4.3).'],
    ['Contraste e layout adaptável', 'Melhora legibilidade e uso em telas estreitas (1.4.3; 1.4.10).']
], [175, 324])
add('Foram usados controles HTML nativos. O tabindex=-1 permite foco programático no conteúdo e nos títulos sem alterar a sequência normal do Tab. ARIA foi utilizado para complementar nomes e avisos dinâmicos, sem substituir a semântica HTML.', 'SmallText')
story.append(PageBreak())

title('5. Carrinho e navegação')
shot('depois-carrinho-preenchido.png', 'Figura 4. Carrinho com dois títulos e três exemplares. Foco no título após navegar.', 260)
shot('depois-carrinho-vazio.png', 'Figura 5. Carrinho após remover o último título. O foco retorna ao h1.', 220)
add('A regra do código base foi preservada: remover um título elimina todas as cópias desse livro. A versão melhorada agrupa as cópias, mostra a quantidade e fornece um nome acessível que explicita a remoção de todas elas.')
add('Ao mudar de rota, o título do documento é atualizado e o foco vai ao título principal. Após uma remoção, o foco retorna ao título do carrinho, evitando que desapareça junto com o botão removido. Os avisos de adição e remoção usam role=status, aria-live=polite e aria-atomic=true.')
story.append(PageBreak())

title('6. Auditorias antes e depois')
shot('antes-catalogo-lighthouse.png', 'Figura 6. Relatório inicial do catálogo: 84/100. O arquivo original HTML/JSON está no GitHub.', 250)
shot('depois-catalogo-lighthouse.png', 'Figura 7. Relatório final do catálogo: 100/100. Os itens de verificação manual continuam indicados pela ferramenta.', 250)
add('O carrinho vazio passou de 79/100 para 100/100. Seus relatórios e prints também estão na pasta evidencias. O estado preenchido foi verificado no fluxo de teclado, e não na navegação padrão do Lighthouse, que recarrega a aplicação e esvazia o estado em memória.')
add('Durante a implementação, o Lighthouse identificou um aviso de diferença entre o texto visível e o nome acessível dos botões, mesmo com nota 100. Os nomes foram corrigidos para começar pelo texto visível completo; a auditoria do catálogo foi repetida sem esse aviso.', 'SmallText')
story.append(PageBreak())

title('7. Testes e limites da avaliação')
section('Teclado e comportamento')
for result in keyboard['results']:
    add(f'<b>{escape(result["name"])}:</b> {escape(result["detail"])}', 'SmallText')
add('Os sete registros acima passaram no teste automatizado com teclas simuladas no Chrome. Os três testes do Redux também passaram: adicionar cópias sem alterar o estado anterior; remover todas as cópias do título e preservar os demais; remover o último livro e preservar ações desconhecidas. O build foi concluído.')
section('Verificação com NVDA')
if nvda:
    add(escape(nvda['summary']))
    add('Registro fornecido pelo aluno: ' + escape(nvda['observations']), 'SmallText')
else:
    add('<b>Pendente de confirmação da leitura.</b> O NVDA 2026.3 foi baixado da fonte oficial, com assinatura válida de NV Access Limited, e iniciado em cópia portátil. A automação de janelas não conseguiu concluir a interação com as boas-vindas. Não foi possível confirmar anúncios da livraria; a inicialização do programa não foi tratada como teste aprovado.')
    add('Roteiro para concluir: abrir a livraria no Chrome com o NVDA ativo; verificar títulos e capas; percorrer os controles com Tab e Shift+Tab; adicionar livros com Enter e Espaço; conferir os anúncios de adição, total, troca para o carrinho, remoção e estado vazio. Registrar o que foi ouvido e, se possível, uma captura real do Visualizador de fala. O roteiro completo está em docs/TESTE-NVDA.md.', 'SmallText')
section('Limitações e conclusão')
add('As auditorias automáticas e o fluxo de teclado mostram melhorias na estrutura, orientação e operação do carrinho. A presença de uma região de status no DOM não prova que um leitor de tela anunciou seu conteúdo. Não foram realizados teste de zoom real, avaliação com usuários com deficiência ou análise integral de todos os critérios WCAG 2.2. Não se declara certificação de conformidade.')
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
