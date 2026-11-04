# -*- coding: utf-8 -*-
"""Lot images novembre 2026 : corps, instruments, races, aliments, tableaux.
Images libres de Wikimedia Commons, verifiees une par une (photos sans texte)."""
import json, sys, urllib.parse
from candidats_img_nov import C

choix = json.load(open(sys.argv[1], encoding="utf-8"))
QUESTIONS = {"corps": "Quel est cet organe ou cette partie du corps ?",
             "instruments": "Quel est cet instrument de musique ?",
             "races": "Quelle race de chien ou de chat est-ce ? / Which dog or cat breed?",
             "aliments": "Quel est ce fruit ou légume ?",
             "tableaux": "Quel est ce tableau ?"}
EXTRA_ALIAS = {"mandole": ["mandoline"], "sloughi": ["lévrier", "levrier"]}
out = []
for cat, rep, al, dif, titre in C:
    f = choix.get(rep)
    if not f:
        continue
    al = [a for a in al if a != "tabla" or rep == "tabla"] + EXTRA_ALIAS.get(rep, [])
    url = ("https://commons.wikimedia.org/wiki/Special:FilePath/"
           + urllib.parse.quote(f, safe="") + "?width=500")
    out.append({"categorie": cat, "difficulte": dif, "question": QUESTIONS[cat],
                "reponse": rep, "alias": al, "url_image": url, "sujet_image": rep})
json.dump(out, open("lot_images_nov.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
print(len(out), Counter(x["categorie"] for x in out))
