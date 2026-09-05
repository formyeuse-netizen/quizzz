"""
Serveur du jeu de quiz.

Lancement :
    py -m pip install fastapi uvicorn
    py serveur.py

Puis ouvre http://localhost:8000 dans ton navigateur.
"""

import asyncio
import json
import random
import sqlite3
import string
import time

import os

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from matching import verifier_reponse

# --- Regles du jeu ---------------------------------------------------------

DUREE_MANCHE = 20           # secondes par question
FENETRE_APRES_PREMIER = 10  # temps laisse aux autres apres la 1re bonne reponse
OBJECTIF = 100              # score qui met fin a la partie
PAUSE_ENTRE_MANCHES = 5     # secondes d'affichage de la reponse
BONUS_PREMIER = 2           # points supplementaires pour celui qui trouve en 1er
JOUEURS_MAX = 10
DELAI_RECONNEXION = 30      # secondes avant d'evincer un joueur deconnecte

BASE = "questions.db"

CATEGORIES = ["algerie", "football", "nba", "sport", "anime",
              "film", "series", "culture_g", "geographie", "histoire", "physique",
              "musique"]
DIFFICULTES = ["facile", "moyen", "difficile"]

app = FastAPI()
salons = {}

# Sert les images locales : depose tes photos dans un dossier "images"
# a cote de serveur.py, puis reference-les avec "/images/ta_photo.jpg".
os.makedirs("images", exist_ok=True)
app.mount("/images", StaticFiles(directory="images"), name="images")


def points_pour(secondes):
    """10 points si instantane, 1 point si on repond a la derniere seconde."""
    part = min(max(secondes / DUREE_MANCHE, 0), 1)
    return max(1, round(10 - 9 * part))


# --- Acces aux questions ---------------------------------------------------

def piocher(categories, difficultes, deja_posees):
    conn = sqlite3.connect(BASE)
    conn.row_factory = sqlite3.Row
    trous_cat = ",".join("?" * len(categories))
    trous_dif = ",".join("?" * len(difficultes))
    requete = (f"SELECT id, question, reponse, alias, categorie, difficulte, "
               f"avec_image, url_image, sujet_image "
               f"FROM questions WHERE categorie IN ({trous_cat}) "
               f"AND difficulte IN ({trous_dif})")
    params = list(categories) + list(difficultes)
    if deja_posees:
        requete += f" AND id NOT IN ({','.join('?' * len(deja_posees))})"
        params += list(deja_posees)
    requete += " ORDER BY RANDOM() LIMIT 1"
    ligne = conn.execute(requete, params).fetchone()
    conn.close()
    if not ligne:
        return None
    return {
        "id": ligne["id"],
        "question": ligne["question"],
        "reponse": ligne["reponse"],
        "alias": json.loads(ligne["alias"]),
        "categorie": ligne["categorie"],
        "difficulte": ligne["difficulte"],
        "avec_image": ligne["avec_image"],
        "image": ligne["url_image"] if ligne["avec_image"] else "",
        "sujet_image": ligne["sujet_image"] or "",
    }


def signaler_question(qid):
    conn = sqlite3.connect(BASE)
    conn.execute("UPDATE questions SET signalements = signalements + 1 "
                 "WHERE id = ?", (qid,))
    conn.commit()
    conn.close()


# --- Salon -----------------------------------------------------------------

class Salon:
    def __init__(self, code):
        self.code = code
        self.joueurs = {}          # jeton -> dict
        self.hote = None
        self.categories = list(CATEGORIES)
        self.difficultes = list(DIFFICULTES)
        self.etat = "salon"        # salon | manche | pause | fini
        self.question = None
        self.debut = 0
        self.fin_prevue = 0
        self.premier = None
        self.deja_posees = []
        self.numero = 0
        self.boucle = None

    # -- joueurs --

    def liste_joueurs(self):
        return [
            {"pseudo": j["pseudo"], "score": j["score"],
             "connecte": j["ws"] is not None, "hote": jeton == self.hote,
             "trouve": j.get("trouve", False)}
            for jeton, j in sorted(self.joueurs.items(),
                                   key=lambda x: -x[1]["score"])
        ]

    def actifs(self):
        return [j for j in self.joueurs.values() if j["ws"] is not None]

    # -- envoi --

    async def envoyer(self, joueur, message):
        ws = joueur.get("ws")
        if ws is None:
            return
        try:
            await ws.send_text(json.dumps(message, ensure_ascii=False))
        except Exception:
            joueur["ws"] = None

    async def diffuser(self, message):
        for joueur in list(self.joueurs.values()):
            await self.envoyer(joueur, message)

    async def diffuser_etat(self):
        await self.diffuser({
            "type": "salon",
            "code": self.code,
            "etat": self.etat,
            "joueurs": self.liste_joueurs(),
            "categories": self.categories,
            "difficultes": self.difficultes,
            "objectif": OBJECTIF,
        })

    # -- partie --

    async def jouer(self):
        try:
            while self.etat != "fini":
                question = piocher(self.categories, self.difficultes,
                                   self.deja_posees)
                if question is None:
                    # Banque epuisee : on repart sur l'ensemble des questions.
                    self.deja_posees = []
                    question = piocher(self.categories, self.difficultes, [])
                if question is None:
                    await self.diffuser({
                        "type": "erreur",
                        "message": "Aucune question pour ces categories."})
                    self.etat = "salon"
                    await self.diffuser_etat()
                    return

                self.numero += 1
                self.question = question
                self.deja_posees.append(question["id"])
                self.premier = None
                self.debut = time.time()
                self.fin_prevue = self.debut + DUREE_MANCHE
                self.etat = "manche"
                for j in self.joueurs.values():
                    j["trouve"] = False

                await self.diffuser({
                    "type": "manche",
                    "numero": self.numero,
                    "question": question["question"],
                    "categorie": question["categorie"],
                    "difficulte": question["difficulte"],
                    "duree": DUREE_MANCHE,
                    "image": question.get("image", ""),
                })

                while time.time() < self.fin_prevue:
                    presents = self.actifs()
                    if presents and all(j.get("trouve") for j in presents):
                        break
                    await asyncio.sleep(0.1)

                self.etat = "pause"
                await self.diffuser({
                    "type": "fin_manche",
                    "reponse": question["reponse"],
                    "joueurs": self.liste_joueurs(),
                })

                meilleur = max((j["score"] for j in self.joueurs.values()),
                               default=0)
                if meilleur >= OBJECTIF:
                    self.etat = "fini"
                    await self.diffuser({
                        "type": "fin_partie",
                        "joueurs": self.liste_joueurs(),
                    })
                    return

                await asyncio.sleep(PAUSE_ENTRE_MANCHES)
        except asyncio.CancelledError:
            raise
        except Exception as e:
            await self.diffuser({"type": "erreur", "message": str(e)})
            self.etat = "salon"
            await self.diffuser_etat()

    async def traiter_reponse(self, jeton, texte):
        if self.etat != "manche" or not self.question:
            return
        joueur = self.joueurs.get(jeton)
        if not joueur or joueur.get("trouve"):
            return

        if not verifier_reponse(texte, self.question["reponse"],
                                self.question["alias"]):
            await self.envoyer(joueur, {"type": "rate"})
            # On montre l'essai rate a tout le monde (le fil des reponses).
            essai = (texte or "").strip()[:40]
            if essai:
                await self.diffuser({
                    "type": "essai",
                    "pseudo": joueur["pseudo"],
                    "texte": essai,
                    "bon": False,
                })
            return

        ecoule = time.time() - self.debut
        gagnes = points_pour(ecoule)
        premier = self.premier is None
        if premier:
            self.premier = jeton
            gagnes += BONUS_PREMIER
            # La manche se termine 10 s plus tard, sans depasser la duree prevue.
            self.fin_prevue = min(time.time() + FENETRE_APRES_PREMIER,
                                  self.debut + DUREE_MANCHE)

        joueur["score"] += gagnes
        joueur["trouve"] = True

        # Bonne reponse : on l'annonce dans le fil SANS reveler le mot.
        await self.diffuser({
            "type": "essai",
            "pseudo": joueur["pseudo"],
            "bon": True,
        })

        await self.envoyer(joueur, {
            "type": "trouve", "points": gagnes, "premier": premier})
        await self.diffuser({
            "type": "quelquun_a_trouve",
            "pseudo": joueur["pseudo"],
            "premier": premier,
            "fin_dans": max(0, round(self.fin_prevue - time.time())),
            "joueurs": self.liste_joueurs(),
        })


def nouveau_code():
    while True:
        code = "".join(random.choices(string.ascii_uppercase, k=4))
        if code not in salons:
            return code


# --- Routes ----------------------------------------------------------------

@app.get("/")
async def accueil():
    return FileResponse("index.html")


@app.websocket("/ws")
async def websocket(ws: WebSocket):
    await ws.accept()
    salon = None
    jeton = None

    try:
        while True:
            message = json.loads(await ws.receive_text())
            action = message.get("type")

            # --- entrer dans un salon ---
            if action in ("creer", "rejoindre") and salon is None:
                pseudo = (message.get("pseudo") or "").strip()[:16]
                jeton = message.get("jeton") or ""
                if not pseudo or not jeton:
                    await ws.send_text(json.dumps({
                        "type": "erreur", "message": "Choisis un pseudo."}))
                    continue

                if action == "creer":
                    code = nouveau_code()
                    salons[code] = Salon(code)
                    salon = salons[code]
                    salon.hote = jeton
                else:
                    code = (message.get("code") or "").strip().upper()
                    salon = salons.get(code)
                    if salon is None:
                        await ws.send_text(json.dumps({
                            "type": "erreur",
                            "message": "Ce code ne correspond a aucun salon."}))
                        continue
                    if (jeton not in salon.joueurs
                            and len(salon.joueurs) >= JOUEURS_MAX):
                        await ws.send_text(json.dumps({
                            "type": "erreur", "message": "Le salon est plein."}))
                        salon = None
                        continue

                if jeton in salon.joueurs:
                    # Reconnexion : on recupere le score.
                    salon.joueurs[jeton]["ws"] = ws
                    salon.joueurs[jeton]["pseudo"] = pseudo
                else:
                    salon.joueurs[jeton] = {
                        "pseudo": pseudo, "score": 0, "ws": ws, "trouve": False}
                if salon.hote not in salon.joueurs:
                    salon.hote = jeton

                await ws.send_text(json.dumps({
                    "type": "entre", "code": salon.code, "jeton": jeton}))
                await salon.diffuser_etat()

                # Le retardataire recupere la manche en cours.
                if salon.etat == "manche" and salon.question:
                    await salon.envoyer(salon.joueurs[jeton], {
                        "type": "manche",
                        "numero": salon.numero,
                        "question": salon.question["question"],
                        "categorie": salon.question["categorie"],
                        "difficulte": salon.question["difficulte"],
                        "duree": max(0, round(salon.fin_prevue - time.time())),
                        "image": salon.question.get("image", ""),
                    })
                continue

            if salon is None:
                continue

            # --- reglages, reserves a l'hote ---
            if action == "reglages" and jeton == salon.hote:
                cats = [c for c in message.get("categories", [])
                        if c in CATEGORIES]
                difs = [d for d in message.get("difficultes", [])
                        if d in DIFFICULTES]
                salon.categories = cats or list(CATEGORIES)
                salon.difficultes = difs or list(DIFFICULTES)
                await salon.diffuser_etat()

            elif action == "demarrer" and jeton == salon.hote:
                if salon.etat in ("salon", "fini"):
                    for j in salon.joueurs.values():
                        j["score"] = 0
                        j["trouve"] = False
                    salon.deja_posees = []
                    salon.numero = 0
                    salon.boucle = asyncio.create_task(salon.jouer())

            elif action == "reponse":
                await salon.traiter_reponse(jeton, message.get("texte", ""))

            elif action == "signaler":
                if salon.question:
                    signaler_question(salon.question["id"])

    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        if salon and jeton in salon.joueurs:
            salon.joueurs[jeton]["ws"] = None
            try:
                await salon.diffuser_etat()
            except Exception:
                pass
            # Salon vide : on le supprime apres le delai de reconnexion.
            if not salon.actifs():
                await asyncio.sleep(DELAI_RECONNEXION)
                if salon.code in salons and not salon.actifs():
                    if salon.boucle:
                        salon.boucle.cancel()
                    salons.pop(salon.code, None)


if __name__ == "__main__":
    import socket
    import uvicorn

    try:
        ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        ip = "ton-ip-locale"

    print("\n" + "=" * 52)
    print("  Serveur lance.")
    print(f"  Sur ce PC        : http://localhost:8000")
    print(f"  Sur le wifi      : http://{ip}:8000")
    print("  Arreter          : Ctrl + C")
    print("=" * 52 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")
