import { chromium } from 'playwright';

const browser = await chromium.launch({ channel: 'chrome', headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  for (const [route, name, height] of [['/', 'catalogo', 220], ['/cart', 'carrinho', 110]]) {
    await page.goto(`http://127.0.0.1:5175${route}`, { waitUntil: 'networkidle' });
    await page.getByRole('heading').first().waitFor();
    await page.screenshot({ path: `evidencias/antes-${name}-detalhe.png`, clip: { x: 0, y: 0, width: 600, height } });
  }
} finally { await browser.close(); }
