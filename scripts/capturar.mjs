import { chromium } from 'playwright';
import { resolve } from 'node:path';

const [url, name] = process.argv.slice(2);
const browser = await chromium.launch({ channel: 'chrome', headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.locator('img').evaluateAll(images => Promise.all(images.map(image => image.decode())));
  await page.getByRole('heading').first().waitFor();
  await page.screenshot({ path: resolve(`evidencias/${name}.png`), fullPage: true });
  console.log({ url: page.url(), title: await page.title(), screenshot: `${name}.png` });
} finally {
  await browser.close();
}
