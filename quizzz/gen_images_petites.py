# -*- coding: utf-8 -*-
"""Lot images "petites categories" (nov. 2026). Images libres (Wikimedia
Commons), verifiees une par une dans le navigateur."""
import json, urllib.parse
from candidats_img_petites import C

choix = json.load(open("choix_images_petites.json", encoding="utf-8"))
Q = {"races": "Quelle race de chien ou de chat est-ce ? / Which dog or cat breed?",
     "tableaux": "Quel est ce tableau ?", "instruments": "Quel est cet instrument de musique ?",
     "aliments": "Quel est ce fruit ou légume ?", "voitures": "Quel est ce modèle de voiture ?",
     "logos": "Quel est ce logo ?", "corps": "Quel est cet organe ou cette partie du corps ?"}
# Ajustements apres verification des images
REMPLACE = {
    "L'Été": ("Le Printemps (Arcimboldo)", ["le printemps", "printemps", "arcimboldo"]),
    "tambourin": ("tambourin", ["tambour de basque", "tambourine", "pandeiro", "tambour"]),
    "noix de cajou": ("noix de cajou", ["cajou", "anacarde", "pomme de cajou"]),
    "Nintendo": ("Nintendo Switch", ["switch", "nintendo"]),
    "Microsoft": ("Microsoft", ["windows"]),
    "Opel": ("Opel", ["opel blitz"]),
}
Q_SPECIALE = {"aliments": {"anis étoilé", "cannelle", "clou de girofle", "cardamome", "vanille",
                           "noix de cajou", "noix de pécan", "noix du Brésil", "noix de macadamia",
                           "pignon de pin", "quinoa", "edamame", "haricot rouge"}}
out = []
for i, (cat, rep, al, dif, fr, en) in enumerate(C):
    f = choix.get(str(i))
    if not f:
        continue
    if rep in REMPLACE:
        rep, al = REMPLACE[rep]
    q = Q[cat]
    if rep in Q_SPECIALE.get(cat, ()):
        q = "Quel est cet aliment ?"
    url = ("https://commons.wikimedia.org/wiki/Special:FilePath/"
           + urllib.parse.quote(f, safe="") + "?width=500")
    out.append({"categorie": cat, "difficulte": dif, "question": q, "reponse": rep,
                "alias": al, "url_image": url, "sujet_image": rep})
json.dump(out, open("lot_images_petites.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
print(len(out), Counter(x["categorie"] for x in out))
