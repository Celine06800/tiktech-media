# TikTech IA · vidéos TikTok

Compte TikTok **@tiktech.info.ia** (« TikTech · L'IA concrète »), média édité par **SEECLICK**.
Ce dépôt héberge les vidéos (muettes) et leurs sources. Lien de la bio : https://www.seeclick.fr/liens
Metricool : marque « TikTech », brandId 8053508, pour les statistiques (la publication se fait depuis l'appli TikTok pour les sons tendance).

## Ligne éditoriale (validée par Céline le 11/11/2026)

**« 1 outil, 1 problème réglé, chaque jour. »** Une vidéo par jour, 20 à 25 s, 1080 × 1920, sans visage,
tout le texte à l'écran, **sans musique** (Céline ajoute un son tendance TikTok en publiant).
Publication par Céline depuis l'appli : 12 h 30 en semaine, 10 h le dimanche.

| Jour | Domaine | Contenu |
|---|---|---|
| Lundi | Direction et pilotage | Tip IA |
| Mardi | Marketing | Tip IA |
| Mercredi | Commercial | Tip IA |
| Jeudi | RH et formation | **Outil SEECLICK** : RH Facility (semaines paires) / Opilot (semaines impaires) |
| Vendredi | Production et terrain | Tip IA |
| Samedi | Admin et finance | **Outil SEECLICK** : Neotech, avocat solo (semaines paires) / Kazaia, le dirigeant côté perso (semaines impaires) |
| Dimanche | « Le minimum IA » | Ce que tout entrepreneur devrait faire, en alternance avec « À la pointe » (actu IA expliquée) |

**Métiers en rotation** : BTP, industrie, coiffure, esthétique, restauration, commerce, artisans, professions
libérales, immobilier, transport, santé et bien-être, formateurs… Une vidéo = un métier visible dans l'accroche.
Ne jamais répéter un couple domaine × métier déjà dans `journal.md`.

**Cibles des outils SEECLICK** : RH Facility = toute entreprise qui a des salariés ; Opilot = formateurs ou
personnes qui veulent le devenir (Qualiopi) ; Neotech (NeoDesk, NeoVoice…) = avocats solo ; Kazaia = particuliers
(les papiers du foyer).

**Message de fond, régulièrement** : « Ton métier n'a pas son outil ? SEECLICK le crée sur mesure. »

**Noël (décision du 12/11/2026)** : du 21 au 31 décembre seulement, un clin d'œil discret de Noël dans les vidéos
(quelques flocons ou une lumière dorée, une accroche de saison), sans changer l'identité nuit et cyan. Le reste de l'année : aucun décor de saison.

## Structure d'une vidéo

1. Accroche métier lisible dès la 1re image (sert de couverture).
2. Bascule : la solution (tip ou outil SEECLICK nommé).
3. La solution en 3 gestes, avec un élément d'interface animé (données fictives, marquées « Exemple fictif »).
4. Point de vigilance ou élargissement (relecture humaine, données clients, « dès le 1er salarié »…).
5. Fin : appel à l'action + « 👉 lien en bio » + logo SEECLICK.

## Règles

- Tutoiement. Aucun gain chiffré ni durée promis : un exemple n'est jamais une promesse.
- Tips : gestes avec « ton IA » (ChatGPT, Claude, Mistral, Gemini… n'importe laquelle), sans mettre en avant un
  outil concurrent des outils SEECLICK.
- Outils SEECLICK : chaque fonction citée est vérifiée dans le code du dépôt de l'outil (ou son site) ; prix HT/TTC
  précisé si cité. Neotech : données fictives, rien qui touche au secret professionnel.
- Diagnostic SEECLICK : « sans engagement, réponse sous 48 h » (jamais « gratuit »). Audit RH Facility : gratuit, 10 questions, 3 min.
- Les liens écrits dans une description TikTok ne sont pas cliquables : toujours « 👉 lien en bio ».
- Espaces insécables avant ? ! : » et après «, et entre un nombre et son unité ; aucun mot seul en fin de ligne.
- Zone sûre TikTok : texte entre 300 et 1450 px de haut, rien dans les 120 px de droite.

## Outils

```bash
node outils/apercu.mjs sources/<fichier>.html /tmp/apercu 0 3 7 15 19 22.4   # images de contrôle
node outils/render.mjs sources/<fichier>.html 23.2 media/<fichier>.mp4        # MP4 muet 30 i/s
```

Gabarit : copier une page de `sources/` (`outils/tiktech.css` pour la charte nuit #070B14 / cyan #22D3EE,
`outils/base.js` pour les animations : `data-in`, `data-out`, `data-anim` = fade, blur, drop, up, left, scale,
words, type, wipe ; `data-shake`, `data-shine`).

Lien de téléchargement d'une vidéo : `https://raw.githubusercontent.com/Celine06800/tiktech-media/main/media/<fichier>.mp4`
