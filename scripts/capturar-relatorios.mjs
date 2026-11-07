import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';

const browser = await chromium.launch({ channel: 'chrome', headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  for (const name of ['antes-catalogo', 'depois-catalogo', 'antes-carrinho', 'depois-carrinho']) {
    await page.goto(pathToFileURL(resolve(`evidencias/${name}.report.html`)).href, { waitUntil: 'networkidle' });
    await page.screenshot({ path: `evidencias/${name}-lighthouse.png` });
    console.log(`${name}: captura do relatório Lighthouse salva`);
  }
} finally { await browser.close(); }
