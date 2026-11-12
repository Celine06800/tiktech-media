// Rend une page HTML de vidéo TikTech (1080×1920, window.render(t)) en MP4 muet, 30 i/s.
// Muet volontairement : Céline ajoute un son tendance dans TikTok au moment de publier.
// Usage : node outils/render.mjs <page.html> <durée_s> <sortie.mp4>
import { createRequire } from "node:module";
import { spawn } from "node:child_process";
import path from "node:path";
const { chromium } = createRequire(import.meta.url)("playwright");
const [page, dureeArg, sortie] = process.argv.slice(2);
if (!page || !dureeArg || !sortie) { console.error("Usage : node outils/render.mjs <page.html> <durée_s> <sortie.mp4>"); process.exit(1); }
const fps = 30, n = Math.round(parseFloat(dureeArg) * fps);
const nav = await chromium.launch();
const p = await nav.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await p.goto("file://" + path.resolve(page), { waitUntil: "networkidle" });
await p.evaluate(() => document.fonts.ready);
const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(fps), "-i", "-",
  "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-crf", "17", "-preset", "slow", "-movflags", "+faststart", sortie],
  { stdio: ["pipe", "inherit", "inherit"] });
const ecran = await p.$(".reel");
for (let i = 0; i < n; i++) {
  await p.evaluate((t) => window.render(t), i / fps);
  const img = await (ecran ?? p).screenshot({ type: "jpeg", quality: 93 });
  if (!ff.stdin.write(img)) await new Promise((r) => ff.stdin.once("drain", r));
}
ff.stdin.end();
await new Promise((r, j) => ff.on("close", (c) => (c === 0 ? r() : j(new Error("ffmpeg " + c)))));
await nav.close();
console.log(`OK ${sortie} (${n} images, muet)`);
