# -*- coding: utf-8 -*-
"""Lot images n°2 (nov. 2026) : Algerie, voitures, espace, nature, sport, cuisine.
Images libres (Wikimedia Commons), verifiees une par une."""
import json, urllib.parse
from candidats_img_nov2 import C

choix = json.load(open("choix_images_nov2.json", encoding="utf-8"))
Q = {("algerie", "lieu"): "Quel est ce lieu d'Algérie ?",
     ("algerie", "plat"): "Quel est ce plat algérien ?",
     ("algerie", "perso"): "Qui est cette personnalité algérienne ?",
     ("voitures", "voiture"): "Quel est ce modèle de voiture ?",
     ("espace", "objet"): "Quel est cet objet céleste ? / What celestial object is this?",
     ("nature", "lieu"): "Quel est ce lieu naturel ?",
     ("sport", "perso"): "Quel sportif est-ce ?",
     ("cuisine", "plat"): "Quel plat est-ce ? / What dish is this?"}
PERSOS_ESPACE = {"Youri Gagarine", "Neil Armstrong", "Valentina Terechkova", "Thomas Pesquet", "Laïka"}
# Ajustements de reponse / alias apres verification des images
REMPLACE = {"apple pie": ("tarte aux pommes", ["apple pie"]),
            "radiotélescope": ("radiotélescope", ["radiotelescope", "radio telescope", "very large array", "vla"]),
            "Apollo 11": ("Apollo 11", ["apollo", "buzz aldrin", "mission apollo", "premier pas sur la lune"]),
            "xiaolongbao": ("xiaolongbao", ["xiao long bao", "dim sum", "raviolis chinois"]),
            "kabsa": ("kabsa", ["machboos", "mandi", "riz au poulet"]),
            "dolma": ("dolma", ["dolmas", "poivrons farcis", "légumes farcis"]),
            "lune de sang": ("éclipse lunaire", ["lune de sang", "eclipse de lune", "eclipse lunaire", "blood moon", "lunar eclipse"])}
out = []
for i, (cat, st, rep, al, dif, fr, en) in enumerate(C):
    f = choix.get(str(i))
    if not f:
        continue
    if rep in REMPLACE:
        rep, al = REMPLACE[rep]
    q = Q[(cat, st)]
    if cat == "espace" and rep in PERSOS_ESPACE:
        q = "Qui est-ce ? (conquête spatiale)"
    url = ("https://commons.wikimedia.org/wiki/Special:FilePath/"
           + urllib.parse.quote(f, safe="") + "?width=500")
    out.append({"categorie": cat, "difficulte": dif, "question": q, "reponse": rep,
                "alias": al, "url_image": url, "sujet_image": rep})
json.dump(out, open("lot_images_nov2.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
print(len(out), Counter(x["categorie"] for x in out))
