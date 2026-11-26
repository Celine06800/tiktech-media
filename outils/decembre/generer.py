"""Génère les pages sources, descriptions et lignes de journal des vidéos TikTech de décembre 2026.
Usage : python3 outils/decembre/generer.py   (depuis la racine du dépôt)"""
import re, sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from contenus import V, TIP_FIN

R = pathlib.Path(__file__).resolve().parents[2]
NB, FIN = " ", " "
EPIQUE = sorted(p.name for p in (R / "outils/sons/epique").glob("*.mp3"))

def fr(s):
    """Typographie française dans le texte (hors balises)."""
    parts = re.split(r"(<[^>]+>)", s)
    out = []
    for p in parts:
        if p.startswith("<"):
            out.append(p); continue
        p = re.sub(r" ([?!:;»])", FIN + r"\1", p)
        p = p.replace("« ", "«" + FIN).replace("e-mail", "e\u2011mail")
        p = re.sub(r"(\d) (€|%|h|min|km|ans|mois|jours|vol|pers\.|lignes|posts|cm)\b", r"\1" + NB + r"\2", p)
        p = re.sub(r"(\d) (\d{3})", r"\1" + NB + r"\2", p)
        out.append(p)
    return "".join(out)

def words(s):
    """Élément animé mot à mot : espaces normaux entre les mots, insécable fine seulement avant la ponctuation."""
    return fr(s)

POS = [(0, 0), (300, 110), (40, 230), (330, 350), (10, 470)]
NOEL = """<canvas id="noel" width="1080" height="1920" style="position:absolute;inset:0;pointer-events:none;z-index:0"></canvas>
<script>(function(){const c=document.getElementById('noel'),x=c.getContext('2d');let s=7;const r=()=>((s=(s*16807)%2147483647)/2147483647);
const f=[...Array(46)].map(()=>({x:r()*1080,y:r()*1920,v:25+r()*45,R:1.5+r()*3,o:r()*6}));
window.__noel=function(t){x.clearRect(0,0,1080,1920);const g=x.createRadialGradient(540,-60,0,540,-60,900);g.addColorStop(0,'rgba(255,214,140,.10)');g.addColorStop(1,'rgba(255,214,140,0)');x.fillStyle=g;x.fillRect(0,0,1080,1920);
for(const p of f){const y=(p.y+p.v*t)%1960-20,xx=p.x+Math.sin(t*.8+p.o)*14;x.globalAlpha=.35+.25*Math.sin(t*2+p.o);x.fillStyle='#fff';x.beginPath();x.arc(xx,y,p.R,0,7);x.fill();}x.globalAlpha=1;};})();</script>"""

def page(v):
    d = dict(TIP_FIN); d.update({k: v[k] for k in v})
    noel = v["date"] >= "2026-12-21"
    bulles = "\n".join(
        f'    <div class="bulle" style="position:absolute;left:{l}px;top:{t}px" data-in="{.4+.4*i:.1f}" data-anim="drop"'
        + (' data-shake="2.6,3.8"' if i == 4 else "") + f">{fr(b)}</div>"
        for i, ((l, t), b) in enumerate(zip(POS, v["bulles"])))
    lignes = []
    for i, (txt, cls, tag) in enumerate(v["lignes"]):
        tin = 10.4 + .5 * i
        shine = f' data-shine="{tin+.9:.1f}"' if i == len(v["lignes"]) - 1 else ""
        lignes.append(f'    <div class="ligne" data-in="{tin:.1f}" data-anim="left"{shine}>{fr(txt)}<span class="tag {cls}">{fr(tag)}</span></div>')
    if v.get("fictif"):
        lignes.append('    <div class="fictif" data-in="12.2">Exemple fictif</div>')
    f_texte = f'\n  <div class="texte" style="margin-top:30px" data-in="20.8">{fr(d["f_texte"])}</div>' if d.get("f_texte") else ""
    v2cls = "titre c"
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><link rel="stylesheet" href="../outils/tiktech.css"><style>.etape,.titre,.moyen,.texte{{text-wrap:balance}}</style></head>
<body><div class="reel"><div class="grille"></div>{NOEL if noel else ""}
<div class="marque"><i></i>TikTech IA</div>

<!-- 1. Accroche -->
<div class="scene" data-in="-1" data-dur="0.01" data-out="3.9" data-anim="fade">
  <div class="sur">{fr(v["sur"])}</div>
  <div class="titre">{fr(v["titre"])}</div>
  <div style="position:relative;margin-top:90px;height:600px;white-space:nowrap">
{bulles}
  </div>
</div>

<!-- 2. Bascule -->
<div class="scene" data-in="4" data-out="7.6" data-anim="blur">
  <div class="moyen" data-in="4.1" data-anim="words" data-dur="1">{words(v["b_moyen"])}</div>
  <div class="titre" style="margin-top:20px" data-in="5.1" data-anim="blur">{fr(v["b_titre"])}</div>
  <div class="filet" data-in="6" data-anim="wipe"></div>
  <div class="texte" data-in="6.2">{fr(v["b_texte"])}</div>
</div>

<!-- 3. Méthode -->
<div class="scene" data-in="7.7" data-out="16.6" data-anim="fade">
  <div class="etape" data-in="7.9" data-anim="left"><b>1</b>{fr(v["e1"])}</div>
  <div class="etape" data-in="8.9" data-anim="left"><b>2</b>{fr(v["e2"])}</div>
  <div class="carte on" style="margin:0 0 44px" data-in="9.8" data-anim="scale">
    <div class="lab">{fr(v["lab"])}</div>
{chr(10).join(lignes)}
  </div>
  <div class="etape" data-in="13.6" data-anim="left"><b>3</b>{fr(v["e3"])}</div>
</div>

<!-- 4. Vigilance -->
<div class="scene" data-in="16.7" data-out="19.8" data-anim="blur">
  <div class="{v["v1c"]}" data-in="16.8" data-anim="words" data-dur="1">{words(v["v1"])}</div>
  <div class="{v2cls}" data-in="17.8" data-anim="blur">{fr(v["v2"])}</div>
  <div class="texte" style="margin-top:44px" data-in="18.4">{fr(v["v_texte"])}</div>
</div>

<!-- 5. Fin -->
<div class="scene fin" data-in="19.9" data-anim="fade">
  <div class="moyen" data-in="20" data-anim="words" data-dur=".9">{fr(d["f_moyen"])}</div>{f_texte}
  <div style="margin-top:50px" data-in="21.3" data-anim="scale"><span class="bouton">{fr(d["f_bouton"])}</span></div>
  <div class="texte" style="margin-top:30px" data-in="21.5">{fr(d["f_sous"])}</div>
  <div class="par" style="margin-top:60px" data-in="21.7">{"par" if v.get("f_bouton") else "avec"} <img src="../outils/seeclick.svg" alt="SEECLICK"></div>
</div>
</div>
<script src="../outils/base.js"></script>{"<script>(function(){const r=window.render;window.render=function(t){window.__noel&&window.__noel(t);return r&&r(t);};})();</script>" if noel else ""}</body></html>
"""

def main(only=None):
    plan = []
    for i, v in enumerate(V):
        if only and v["date"] not in only: continue
        nom = f'{v["date"]}-{v["nom"]}'
        (R / "sources" / f"{nom}.html").write_text(page(v))
        desc = v["desc"].rstrip()
        if not desc.endswith("👉 lien en bio"): desc += "\n👉 lien en bio"
        (R / "descriptions" / f'{v["date"]}.md').write_text(f"{desc}\n\n{v['tags']}\n")
        son = EPIQUE[(i * 5) % len(EPIQUE)]
        plan.append(dict(date=v["date"], nom=nom, son=son, titre=v["tt"], texte=f"{desc}\n\n{v['tags']}",
                         dom=v["dom"], metier=v["metier"], outil=v["outil"]))
    (R / "outils/decembre/plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1))
    print(len(plan), "vidéos")

if __name__ == "__main__":
    main(set(sys.argv[1:]) or None)
