// Images de contrôle d'une page vidéo à des instants donnés.
// Usage : node outils/apercu.mjs <page.html> <préfixe_sortie> t1 t2 …   →  <préfixe>-<t>.png
import { createRequire } from "node:module";
import path from "node:path";
const { chromium } = createRequire(import.meta.url)("playwright");
const [page, out, ...ts] = process.argv.slice(2);
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.goto("file://" + path.resolve(page)); await p.evaluate(() => document.fonts.ready);
for (const t of ts) { await p.evaluate((t) => { for (let x = 0; x <= t; x += 0.25) window.render(x); window.render(t); }, parseFloat(t)); await p.screenshot({ path: `${out}-${t}.png` }); }
await b.close();
