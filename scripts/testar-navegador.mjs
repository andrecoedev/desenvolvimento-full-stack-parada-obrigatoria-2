import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { writeFile } from 'node:fs/promises';

const browser = await chromium.launch({ channel: 'chrome', headless: true });
const results = [];
const record = (name, detail) => results.push({ name, result: 'PASS', detail });
try {
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto('http://127.0.0.1:5174/', { waitUntil: 'networkidle' });
  await page.locator('img').evaluateAll(images => Promise.all(images.map(image => image.decode())));
  await page.getByRole('heading', { level: 1 }).waitFor();
  await page.screenshot({ path: 'evidencias/depois-catalogo.png', fullPage: true });

  async function checkFocus(selector) {
    assert.equal(await page.locator(selector).evaluate(element => element === document.activeElement), true, selector);
  }
  await page.keyboard.press('Tab');
  await checkFocus('.skip-link');
  await page.screenshot({ path: 'evidencias/depois-foco-teclado.png', fullPage: true });
  await page.keyboard.press('Enter');
  await checkFocus('main');
  record('Link para pular navegação', 'Tab focou o link; Enter transferiu o foco à região principal.');

  await page.keyboard.press('Tab');
  await checkFocus('button[aria-label="Adicionar ao carrinho: Book 1"]');
  await page.keyboard.press('Enter');
  await page.getByRole('status').filter({ hasText: 'Total: 1' }).waitFor();
  await page.keyboard.press('Space');
  await page.getByRole('status').filter({ hasText: 'Total: 2' }).waitFor();
  record('Botão com Enter e Espaço', 'Duas cópias adicionadas; status atualizado a cada ação.');
  await page.keyboard.press('Tab');
  await checkFocus('button[aria-label="Adicionar ao carrinho: Book 2"]');
  await page.keyboard.press('Enter');
  await page.getByRole('status').filter({ hasText: 'Total: 3' }).waitFor();

  // Retorno pelo teclado até o link do carrinho, sem clicar.
  await page.keyboard.press('Shift+Tab');
  await page.keyboard.press('Shift+Tab');
  await checkFocus('a[href="/cart"]');
  await page.keyboard.press('Enter');
  await page.getByRole('heading', { name: 'Seu carrinho' }).waitFor();
  await checkFocus('h1');
  assert.equal(await page.title(), 'Carrinho | Livraria online');
  assert.equal(await page.locator('.cart-item').count(), 2);
  assert.equal(await page.getByText('Quantidade: 2', { exact: true }).count(), 1);
  await page.screenshot({ path: 'evidencias/depois-carrinho-preenchido.png', fullPage: true });
  record('Rota e foco', 'Shift+Tab e Enter abriram /cart; foco no h1 e título do documento atualizado.');

  await page.keyboard.press('Tab');
  await checkFocus('button[aria-label="Remover do carrinho: todas as cópias de Book 1"]');
  await page.keyboard.press('Space');
  await page.getByRole('status').filter({ hasText: 'Total: 1' }).waitFor();
  await checkFocus('h1');
  assert.equal(await page.locator('.cart-item').count(), 1);
  record('Remoção de cópias', 'Espaço removeu as duas cópias de Book 1, preservou Book 2 e devolveu foco ao h1.');
  await page.keyboard.press('Tab');
  await page.keyboard.press('Enter');
  await page.getByText('Seu carrinho está vazio.').waitFor();
  await checkFocus('h1');
  await page.screenshot({ path: 'evidencias/depois-carrinho-vazio.png', fullPage: true });
  await page.keyboard.press('Tab');
  await checkFocus('.back-link');
  await page.keyboard.press('Enter');
  await page.getByRole('heading', { name: 'Seu próximo livro está aqui.' }).waitFor();
  await checkFocus('h1');
  record('Carrinho vazio e retorno', 'Último título removido; link de retorno operou com Enter, sem perda de foco.');

  for (const width of [320, 640]) {
    await page.setViewportSize({ width, height: 800 });
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
    await page.screenshot({ path: `evidencias/depois-largura-${width}.png`, fullPage: true });
  }
  record('Refluxo', 'Sem rolagem horizontal nos tamanhos de viewport de 320 e 640 CSS pixels; não substitui teste de zoom real.');
  assert.equal(errors.length, 0, errors.join('\n'));
  record('Execução', 'Nenhum erro JavaScript capturado no fluxo.');
  console.log(results);
} finally {
  await writeFile('evidencias/testes-teclado.json', JSON.stringify({ date: new Date().toISOString(), method: 'Playwright com Chrome real, teclas simuladas; sem NVDA neste teste', results }, null, 2));
  await browser.close();
}
