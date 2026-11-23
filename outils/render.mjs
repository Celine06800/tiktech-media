// Rend une page HTML de vidéo TikTech (1080×1920, window.render(t)) en MP4, 30 i/s, AVEC une musique (depuis le 23/11/2026).
// Musiques : morceaux Pixabay choisis par Céline, découpés en extraits de 30 s dans outils/sons/<style>/ (voir outils/sons/SONS.md).
// Usage : node outils/render.mjs <page.html> <durée_s> <sortie.mp4> [--musique epique|lounge|dance] [--graine <n>] [--son <fichier.mp3>] [--muet]
// Sans --graine, l'extrait tourne chaque jour d'après la date AAAA-MM-JJ du nom de sortie (jamais le même deux jours de suite).
// --musique limite au style ; --son impose un extrait ; --muet garde l'ancien MP4 sans son.
import { createRequire } from "node:module";
import { spawn } from "node:child_process";
import path from "node:path";
const { chromium } = createRequire(import.meta.url)("playwright");
import fs from "node:fs";
import { execFileSync } from "node:child_process";
const argv = process.argv.slice(2);
const opt = (k) => { const i = argv.indexOf(k); return i >= 0 ? argv.splice(i, 2)[1] : undefined; };
const flag = (k) => { const i = argv.indexOf(k); if (i >= 0) { argv.splice(i, 1); return true; } return false; };
const style = opt("--musique"); let graine = opt("--graine"); let son = opt("--son"); const muet = flag("--muet");
const [page, dureeArg, sortie] = argv;
if (!page || !dureeArg || !sortie) { console.error("Usage : node outils/render.mjs <page.html> <durée_s> <sortie.mp4>"); process.exit(1); }
const dossierSons = path.join(path.dirname(new URL(import.meta.url).pathname), "sons");
if (!muet && !son && fs.existsSync(dossierSons)) {
  const styles = style ? [style] : fs.readdirSync(dossierSons).filter((d) => fs.statSync(path.join(dossierSons, d)).isDirectory()).sort();
  const liste = styles.flatMap((s) => fs.existsSync(path.join(dossierSons, s)) ? fs.readdirSync(path.join(dossierSons, s)).filter((f) => f.endsWith(".mp3")).sort().map((f) => path.join(dossierSons, s, f)) : []);
  if (graine === undefined) { const m = path.basename(sortie || "").match(/(\d{4})-(\d{2})-(\d{2})/); graine = m ? Math.round(Date.UTC(+m[1], +m[2] - 1, +m[3]) / 864e5) * 7 : 0; }
  if (liste.length) son = liste[((+graine % liste.length) + liste.length) % liste.length];
}
const fps = 30, n = Math.round(parseFloat(dureeArg) * fps);
const nav = await chromium.launch();
const p = await nav.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await p.goto("file://" + path.resolve(page), { waitUntil: "networkidle" });
await p.evaluate(() => document.fonts.ready);
const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(fps), "-i", "-",
  "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-crf", "17", "-preset", "slow", "-movflags", "+faststart", son ? sortie + ".video.mp4" : sortie],
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
if (son) {
  const d = parseFloat(dureeArg), fin = Math.max(0, d - 1).toFixed(2);
  execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-i", sortie + ".video.mp4", "-i", son, "-map", "0:v", "-map", "1:a",
    "-af", `atrim=0:${d},afade=t=in:st=0:d=0.2,afade=t=out:st=${fin}:d=1,loudnorm=I=-16:TP=-1.5:LRA=9`,
    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", sortie]);
  fs.rmSync(sortie + ".video.mp4");
}
console.log(`OK ${sortie} (${n} images, ${son ? "son " + path.basename(son) : "muet"})`);
