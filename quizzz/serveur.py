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

# --- Modes de jeu ---
MODES = ["basique", "pouvoirs", "equipes", "survie", "blitz", "coop", "chacun",
         "tournoi", "bombe", "quittedouble"]
VIES_SURVIE = 3            # vies de depart en mode survie
DUREE_BLITZ = 8            # chrono court (s) en mode blitz
FENETRE_BLITZ = 4          # fenetre (s) apres la 1re bonne reponse en blitz
MANCHES_BLITZ = 20         # nb de manches par defaut en blitz
DELAI_ANNONCE = 4          # secondes d'affichage des annonces de tournoi
FUSE_MIN = 12              # duree mini (s) de la meche en mode bombe
FUSE_MAX = 22             # duree maxi (s) de la meche en mode bombe
START_QD = 100            # score de depart en mode quitte ou double
MANCHES_QD = 10           # nb de manches par defaut en quitte ou double
DUREE_MISE = 10           # secondes pour choisir sa mise

# --- Pouvoirs (phase 2) ---
SERIE_POUR_CHARGE = 3      # bonnes reponses d'affilee pour gagner 1 charge
COOLDOWN_POUVOIR = 8       # secondes de recharge entre deux pouvoirs
POUVOIRS = ["indice", "gel", "double", "skip"]
DUREE_GEL = 3              # secondes de blocage inflige par le gel

BASE = "questions.db"

CATEGORIES = ["algerie", "football", "nba", "sport", "anime",
              "film", "series", "culture_g", "geographie", "histoire", "physique",
              "musique", "animaux", "voitures", "jeuxvideo", "logos", "drapeaux",
              "aliments", "langues", "corps", "cuisine", "espace", "races",
              "nature", "jeuxsociete", "monuments", "tableaux", "instruments"]
DIFFICULTES = ["facile", "moyen", "difficile"]

app = FastAPI()
salons = {}

# Sert les images locales : depose tes photos dans un dossier "images"
# a cote de serveur.py, puis reference-les avec "/images/ta_photo.jpg".
os.makedirs("images", exist_ok=True)
app.mount("/images", StaticFiles(directory="images"), name="images")


def points_pour(secondes, duree=DUREE_MANCHE):
    """10 points si instantane, 1 point si on repond a la derniere seconde."""
    part = min(max(secondes / duree, 0), 1)
    return max(1, round(10 - 9 * part))


def indice_de(reponse):
    """Masque la reponse en revelant seulement la 1re lettre et la longueur.
    Ex. "The Dark Knight" -> "T•• •••• ••••••" (nb de mots + longueurs visibles)."""
    out = []
    premiere = True
    for ch in reponse:
        if ch.isalnum():
            out.append(ch.upper() if premiere else "•")
            premiere = False
        else:
            out.append(ch)
    return "".join(out)


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
        self.duree = DUREE_MANCHE       # chrono par question (reglable par l'hote)
        self.objectif = OBJECTIF        # score qui met fin a la partie
        self.manches_max = 0            # 0 = illimite (fin au score) ; sinon nb de manches
        self.equipes = False            # mode 2 equipes (Rouge vs Bleu)
        self.mode = "basique"           # basique|equipes|survie|blitz|coop|chacun|tournoi
        self.duree_courante = DUREE_MANCHE
        self.repondeurs = None          # None = tout le monde ; sinon set de jetons autorises
        self.tour_i = 0                 # index du joueur actif en mode "chacun son tour"
        self.mises = {}                 # jeton -> mise (mode quitte ou double)
        self.phase_mise = False         # True pendant la fenetre de mise (QD)
        self.etat = "salon"        # salon | manche | pause | fini
        self.question = None
        self.debut = 0
        self.fin_prevue = 0
        self.premier = None
        self.deja_posees = []
        self.numero = 0
        self.boucle = None
        self.indice_envoye = False
        self.stats = None

    # -- joueurs --

    def liste_joueurs(self):
        return [
            {"pseudo": j["pseudo"], "score": j["score"],
             "connecte": j["ws"] is not None, "hote": jeton == self.hote,
             "trouve": j.get("trouve", False), "equipe": j.get("equipe"),
             "vies": j.get("vies"), "elimine": j.get("elimine", False),
             "charges": j.get("charges", 0)}
            for jeton, j in sorted(self.joueurs.items(),
                                   key=lambda x: -x[1]["score"])
        ]

    def actifs(self):
        return [j for j in self.joueurs.values() if j["ws"] is not None]

    def equilibrer(self):
        """Donne une equipe (A/B) a ceux qui n'en ont pas, en equilibrant."""
        for j in self.joueurs.values():
            if j.get("equipe") not in ("A", "B"):
                a = sum(1 for x in self.joueurs.values() if x.get("equipe") == "A")
                b = sum(1 for x in self.joueurs.values() if x.get("equipe") == "B")
                j["equipe"] = "A" if a <= b else "B"

    def scores_equipes(self):
        a = sum(j["score"] for j in self.joueurs.values() if j.get("equipe") == "A")
        b = sum(j["score"] for j in self.joueurs.values() if j.get("equipe") == "B")
        return {"A": a, "B": b}

    # -- modes --

    def duree_effective(self):
        return DUREE_BLITZ if self.mode == "blitz" else self.duree

    def fenetre_effective(self):
        return FENETRE_BLITZ if self.mode == "blitz" else FENETRE_APRES_PREMIER

    def score_collectif(self):
        return sum(j["score"] for j in self.joueurs.values())

    def en_jeu(self, j):
        """Un joueur qui peut encore repondre (non elimine en survie)."""
        return not (self.mode == "survie" and j.get("elimine"))

    def evaluer_fin(self):
        """Renvoie (fini?, extra) selon le mode."""
        if self.mode == "survie":
            vivants = [j for j in self.joueurs.values() if not j.get("elimine")]
            if len(vivants) == 0 or (len(self.joueurs) >= 2 and len(vivants) <= 1):
                return True, {"survivant": vivants[0]["pseudo"] if vivants else None}
            return False, {}
        if self.mode == "coop":
            s = self.score_collectif()
            if s >= self.objectif:
                return True, {"coop_reussi": True, "collectif": s}
            if self.manches_max and self.numero >= self.manches_max:
                return True, {"coop_reussi": False, "collectif": s}
            return False, {}
        if self.mode == "blitz":
            return (self.numero >= (self.manches_max or MANCHES_BLITZ)), {}
        # basique / equipes
        if self.equipes:
            meilleur = max(self.scores_equipes().values(), default=0)
        else:
            meilleur = max((j["score"] for j in self.joueurs.values()), default=0)
        if meilleur >= self.objectif:
            return True, {}
        if self.manches_max and self.numero >= self.manches_max:
            return True, {}
        return False, {}

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
            "objectif": self.objectif,
            "duree": self.duree,
            "manches_max": self.manches_max,
            "equipes": self.equipes,
            "mode": self.mode,
            "scores_equipes": self.scores_equipes() if self.equipes else None,
        })

    # -- partie --

    async def _run_manche(self, repondeurs=None, ctx=None):
        """Joue UNE manche (pioche, diffusion, attente, pause). repondeurs =
        set de jetons autorises a repondre (None = tous). ctx = champs ajoutes
        aux messages manche/fin_manche. Renvoie False si la banque est vide."""
        ctx = ctx or {}
        question = piocher(self.categories, self.difficultes, self.deja_posees)
        if question is None:
            self.deja_posees = []
            question = piocher(self.categories, self.difficultes, [])
        if question is None:
            await self.diffuser({"type": "erreur",
                                 "message": "Aucune question pour ces categories."})
            self.etat = "salon"
            await self.diffuser_etat()
            return False

        self.numero += 1
        self.question = question
        self.deja_posees.append(question["id"])
        self.premier = None
        self.indice_envoye = False
        self.repondeurs = repondeurs
        duree = self.duree_effective()
        self.duree_courante = duree
        self.debut = time.time()
        self.fin_prevue = self.debut + duree
        self.etat = "manche"
        for j in self.joueurs.values():
            j["trouve"] = False
            j["gel_jusqua"] = 0
            j["double_arme"] = False

        await self.diffuser({
            "type": "manche", "numero": self.numero,
            "question": question["question"], "categorie": question["categorie"],
            "difficulte": question["difficulte"], "duree": duree,
            "image": question.get("image", ""), "mode": self.mode, **ctx,
        })

        def concernes():
            if repondeurs is not None:
                return [self.joueurs[k] for k in repondeurs
                        if k in self.joueurs and self.joueurs[k]["ws"] is not None]
            return [j for j in self.actifs() if self.en_jeu(j)]

        mi_temps = self.debut + duree / 2
        while time.time() < self.fin_prevue:
            presents = concernes()
            if presents and all(j.get("trouve") for j in presents):
                break
            if (not self.indice_envoye and self.premier is None
                    and time.time() >= mi_temps):
                self.indice_envoye = True
                await self.diffuser({"type": "indice",
                                     "indice": indice_de(question["reponse"])})
            await asyncio.sleep(0.1)

        if self.premier is None:
            self.stats["colles"] += 1

        # Survie : perte de vie pour les connectes qui n'ont pas trouve.
        elimines_ce_tour = []
        if self.mode == "survie":
            for j in self.joueurs.values():
                if j.get("elimine") or j["ws"] is None:
                    continue
                if not j.get("trouve"):
                    j["vies"] = max(0, j.get("vies", VIES_SURVIE) - 1)
                    if j["vies"] == 0:
                        j["elimine"] = True
                        elimines_ce_tour.append(j["pseudo"])

        self.etat = "pause"
        await self.diffuser({
            "type": "fin_manche", "reponse": question["reponse"],
            "joueurs": self.liste_joueurs(), "mode": self.mode,
            "collectif": (self.score_collectif() if self.mode == "coop" else None),
            "elimines": elimines_ce_tour or None,
            "scores_equipes": (self.scores_equipes() if self.equipes else None),
            **ctx,
        })
        return True

    async def jouer(self):
        self.stats = {"rapide_pseudo": None, "rapide_temps": None,
                      "firsts": {}, "colles": 0}
        self.tour_i = 0
        try:
            while self.etat != "fini":
                repondeurs, ctx = None, {}
                if self.mode == "chacun":
                    ordre = [k for k in self.joueurs
                             if self.joueurs[k]["ws"] is not None]
                    if not ordre:
                        await asyncio.sleep(0.3)
                        continue
                    actif = ordre[self.tour_i % len(ordre)]
                    self.tour_i += 1
                    repondeurs = {actif}
                    ctx = {"tour": self.joueurs[actif]["pseudo"]}

                ok = await self._run_manche(repondeurs, ctx)
                if not ok:
                    return

                fini, extra = self.evaluer_fin()
                if fini:
                    self.etat = "fini"
                    await self.diffuser({
                        "type": "fin_partie", "joueurs": self.liste_joueurs(),
                        "stats": self.bilan_stats(), "mode": self.mode,
                        "scores_equipes": (self.scores_equipes()
                                           if self.equipes else None),
                        **extra,
                    })
                    return

                await asyncio.sleep(PAUSE_ENTRE_MANCHES)
        except asyncio.CancelledError:
            raise
        except Exception as e:
            await self.diffuser({"type": "erreur", "message": str(e)})
            self.etat = "salon"
            await self.diffuser_etat()

    async def jouer_tournoi(self):
        """Bracket a elimination directe. Matches joues l'un apres l'autre ;
        tout le monde regarde, seuls les 2 duellistes repondent."""
        self.stats = {"rapide_pseudo": None, "rapide_temps": None,
                      "firsts": {}, "colles": 0}
        try:
            vivants = [k for k in self.joueurs if self.joueurs[k]["ws"] is not None]
            if len(vivants) < 2:
                await self.diffuser({"type": "erreur",
                    "message": "Il faut au moins 2 joueurs pour un tournoi."})
                self.etat = "salon"
                await self.diffuser_etat()
                return

            tour = 1
            while len(vivants) > 1:
                random.shuffle(vivants)
                paires, byes, i = [], [], 0
                while i < len(vivants):
                    if i + 1 < len(vivants):
                        paires.append((vivants[i], vivants[i + 1])); i += 2
                    else:
                        byes.append(vivants[i]); i += 1

                self.etat = "pause"
                await self.diffuser({
                    "type": "tournoi_tour", "tour": tour,
                    "paires": [[self.joueurs[a]["pseudo"], self.joueurs[b]["pseudo"]]
                               for a, b in paires],
                    "byes": [self.joueurs[b]["pseudo"] for b in byes],
                })
                await asyncio.sleep(DELAI_ANNONCE)

                gagnants = list(byes)
                for p1, p2 in paires:
                    g = await self._jouer_match(p1, p2)
                    if g is None:
                        return          # partie interrompue (banque vide)
                    gagnants.append(g)
                vivants = [k for k in gagnants if k in self.joueurs]
                if not vivants:
                    break
                tour += 1

            champion = vivants[0] if vivants else None
            self.etat = "fini"
            await self.diffuser({
                "type": "fin_partie", "joueurs": self.liste_joueurs(),
                "stats": self.bilan_stats(), "mode": "tournoi",
                "champion": self.joueurs[champion]["pseudo"] if champion else None,
            })
        except asyncio.CancelledError:
            raise
        except Exception as e:
            await self.diffuser({"type": "erreur", "message": str(e)})
            self.etat = "salon"
            await self.diffuser_etat()

    async def _jouer_match(self, p1, p2):
        """Duel best-of-3 (premier a 2 manches gagnees). Renvoie le jeton
        gagnant, ou None si la banque est vide."""
        self.joueurs[p1]["match"] = 0
        self.joueurs[p2]["match"] = 0
        noms = [self.joueurs[p1]["pseudo"], self.joueurs[p2]["pseudo"]]
        q = 0
        while True:
            q += 1
            avant = {p1: self.joueurs[p1]["score"], p2: self.joueurs[p2]["score"]}
            ctx = {"match": noms,
                   "match_score": [self.joueurs[p1]["match"], self.joueurs[p2]["match"]],
                   "match_q": q}
            ok = await self._run_manche({p1, p2}, ctx)
            if not ok:
                return None
            d1 = self.joueurs[p1]["score"] - avant[p1]
            d2 = self.joueurs[p2]["score"] - avant[p2]
            if d1 > d2:
                self.joueurs[p1]["match"] += 1
            elif d2 > d1:
                self.joueurs[p2]["match"] += 1
            m1, m2 = self.joueurs[p1]["match"], self.joueurs[p2]["match"]
            if (m1 >= 2 or m2 >= 2 or q >= 3) and (m1 != m2 or q >= 6):
                break
            await asyncio.sleep(PAUSE_ENTRE_MANCHES)

        gagnant = p1 if self.joueurs[p1]["match"] >= self.joueurs[p2]["match"] else p2
        perdant = p2 if gagnant == p1 else p1
        self.joueurs[perdant]["elimine"] = True
        self.etat = "pause"
        await self.diffuser({
            "type": "tournoi_match_fin", "noms": noms,
            "gagnant": self.joueurs[gagnant]["pseudo"],
            "perdant": self.joueurs[perdant]["pseudo"],
            "score": [self.joueurs[p1]["match"], self.joueurs[p2]["match"]],
        })
        await asyncio.sleep(DELAI_ANNONCE)
        return gagnant

    async def _manche_bombe(self, holder, bomb_end):
        """Une question posee au porteur de la bombe. La meche (bomb_end) est
        partagee : elle NE se reinitialise PAS entre les passes. Renvoie
        'passed' (bonne reponse), 'timeout' (meche ecoulee) ou 'empty'."""
        question = piocher(self.categories, self.difficultes, self.deja_posees)
        if question is None:
            self.deja_posees = []
            question = piocher(self.categories, self.difficultes, [])
        if question is None:
            await self.diffuser({"type": "erreur",
                                 "message": "Aucune question pour ces categories."})
            self.etat = "salon"
            await self.diffuser_etat()
            return "empty"

        self.numero += 1
        self.question = question
        self.deja_posees.append(question["id"])
        self.premier = None
        self.indice_envoye = False
        self.repondeurs = {holder}
        reste = max(1.0, bomb_end - time.time())
        self.debut = time.time()
        self.duree_courante = reste
        self.fin_prevue = bomb_end
        self.etat = "manche"
        for j in self.joueurs.values():
            j["trouve"] = False
            j["gel_jusqua"] = 0
            j["double_arme"] = False

        await self.diffuser({
            "type": "manche", "numero": self.numero,
            "question": question["question"], "categorie": question["categorie"],
            "difficulte": question["difficulte"], "duree": reste,
            "image": question.get("image", ""), "mode": "bombe",
            "tour": self.joueurs[holder]["pseudo"],
        })

        while time.time() < bomb_end:
            h = self.joueurs.get(holder)
            if h and h.get("trouve"):
                return "passed"
            await asyncio.sleep(0.05)
        return "timeout"

    async def jouer_bombe(self):
        """Patate chaude : le porteur doit repondre pour refiler la bombe. Quand
        la meche (cachee, aleatoire) explose, le porteur du moment perd une vie.
        Dernier joueur en vie gagne."""
        self.stats = {"rapide_pseudo": None, "rapide_temps": None,
                      "firsts": {}, "colles": 0}
        try:
            if len([k for k in self.joueurs if self.joueurs[k]["ws"] is not None]) < 2:
                await self.diffuser({"type": "erreur",
                    "message": "Il faut au moins 2 joueurs pour le mode Bombe."})
                self.etat = "salon"
                await self.diffuser_etat()
                return

            idx = 0
            while True:
                encore = [k for k in self.joueurs if not self.joueurs[k].get("elimine")]
                if len(encore) <= 1:
                    break
                fuse = random.uniform(FUSE_MIN, FUSE_MAX)
                bomb_end = time.time() + fuse
                exploded = None
                while time.time() < bomb_end:
                    vivants = [k for k in self.joueurs
                               if not self.joueurs[k].get("elimine")]
                    if len(vivants) <= 1:
                        break
                    holder = vivants[idx % len(vivants)]
                    res = await self._manche_bombe(holder, bomb_end)
                    if res == "empty":
                        return
                    if res == "passed":
                        idx += 1
                        continue
                    exploded = holder     # timeout : la bombe pete sur le porteur
                    break

                if exploded is not None:
                    h = self.joueurs[exploded]
                    h["vies"] = max(0, h.get("vies", VIES_SURVIE) - 1)
                    if h["vies"] == 0:
                        h["elimine"] = True
                    self.etat = "pause"
                    await self.diffuser({
                        "type": "bombe_explose", "pseudo": h["pseudo"],
                        "vies": h["vies"], "elimine": h["elimine"],
                        "joueurs": self.liste_joueurs(),
                    })
                    await asyncio.sleep(DELAI_ANNONCE)
                    idx += 1

            vivants = [k for k in self.joueurs if not self.joueurs[k].get("elimine")]
            champion = vivants[0] if vivants else None
            self.etat = "fini"
            await self.diffuser({
                "type": "fin_partie", "joueurs": self.liste_joueurs(),
                "stats": self.bilan_stats(), "mode": "bombe",
                "survivant": self.joueurs[champion]["pseudo"] if champion else None,
            })
        except asyncio.CancelledError:
            raise
        except Exception as e:
            await self.diffuser({"type": "erreur", "message": str(e)})
            self.etat = "salon"
            await self.diffuser_etat()

    async def jouer_quittedouble(self):
        """Quitte ou double : chacun part de START_QD points. Avant chaque
        question, on mise une part de son capital ; bonne reponse -> on gagne
        la mise, sinon on la perd (plancher a 0). Meilleur score a la fin."""
        self.stats = {"rapide_pseudo": None, "rapide_temps": None,
                      "firsts": {}, "colles": 0}
        try:
            for j in self.joueurs.values():
                j["score"] = START_QD
            n_max = self.manches_max or MANCHES_QD
            while self.numero < n_max and self.etat != "fini":
                # -- phase de mise --
                self.mises = {}
                self.phase_mise = True
                self.etat = "pause"
                await self.diffuser({
                    "type": "mise_debut", "duree": DUREE_MISE,
                    "manche": self.numero + 1, "manches_max": n_max,
                    "joueurs": self.liste_joueurs(),
                })
                t_fin = time.time() + DUREE_MISE
                while time.time() < t_fin:
                    presents = [k for k, j in self.joueurs.items()
                                if j["ws"] is not None and j["score"] > 0]
                    if presents and all(k in self.mises for k in presents):
                        break
                    await asyncio.sleep(0.1)
                self.phase_mise = False

                # clamp des mises au capital courant (defaut 0 si pas de mise)
                mise_tour = {}
                for k, j in self.joueurs.items():
                    m = max(0, min(int(self.mises.get(k, 0)), j["score"]))
                    mise_tour[k] = m

                # -- question --
                ctx = {"mises": {self.joueurs[k]["pseudo"]: v
                                 for k, v in mise_tour.items() if v > 0}}
                ok = await self._run_manche(None, ctx)
                if not ok:
                    return

                # -- application des mises --
                details = []
                for k, j in self.joueurs.items():
                    m = mise_tour.get(k, 0)
                    if j.get("trouve"):
                        j["score"] += m
                        delta = m
                    else:
                        j["score"] = max(0, j["score"] - m)
                        delta = -m
                    if m > 0 or j["ws"] is not None:
                        details.append({"pseudo": j["pseudo"], "mise": m,
                                        "trouve": bool(j.get("trouve")),
                                        "delta": delta, "score": j["score"]})
                await self.diffuser({
                    "type": "qd_resultat", "details": details,
                    "joueurs": self.liste_joueurs(),
                })
                await asyncio.sleep(PAUSE_ENTRE_MANCHES)

            self.etat = "fini"
            await self.diffuser({
                "type": "fin_partie", "joueurs": self.liste_joueurs(),
                "stats": self.bilan_stats(), "mode": "quittedouble",
            })
        except asyncio.CancelledError:
            raise
        except Exception as e:
            await self.diffuser({"type": "erreur", "message": str(e)})
            self.etat = "salon"
            await self.diffuser_etat()

    def bilan_stats(self):
        s = self.stats or {}
        firsts = s.get("firsts") or {}
        roi = max(firsts.items(), key=lambda x: x[1]) if firsts else None
        return {
            "plus_rapide": ({"pseudo": s["rapide_pseudo"],
                             "temps": round(s["rapide_temps"], 1)}
                            if s.get("rapide_pseudo") else None),
            "roi_premier": ({"pseudo": roi[0], "n": roi[1]} if roi else None),
            "colles": s.get("colles", 0),
        }

    async def traiter_reponse(self, jeton, texte):
        if self.etat != "manche" or not self.question:
            return
        joueur = self.joueurs.get(jeton)
        if not joueur or joueur.get("trouve"):
            return
        if not self.en_jeu(joueur):        # elimine (survie/tournoi) : spectateur
            return
        if self.repondeurs is not None and jeton not in self.repondeurs:
            return                          # pas ton tour (chacun / duel tournoi)
        if time.time() < joueur.get("gel_jusqua", 0):   # gele par un adversaire
            await self.envoyer(joueur, {"type": "gele"})
            return

        if not verifier_reponse(texte, self.question["reponse"],
                                self.question["alias"]):
            await self.envoyer(joueur, {"type": "rate"})
            joueur["serie"] = 0            # une erreur casse la serie
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

        # Mode "quitte ou double" : une bonne reponse marque seulement "trouve".
        # La mise est appliquee en fin de manche (aucun point de vitesse, aucune
        # charge de pouvoir).
        if self.mode == "quittedouble":
            joueur["trouve"] = True
            premier = self.premier is None
            if premier:
                self.premier = jeton
                self.fin_prevue = min(time.time() + self.fenetre_effective(),
                                      self.debut + self.duree_courante)
            if self.stats is not None:
                ec = time.time() - self.debut
                if (self.stats["rapide_temps"] is None
                        or ec < self.stats["rapide_temps"]):
                    self.stats["rapide_temps"] = ec
                    self.stats["rapide_pseudo"] = joueur["pseudo"]
                if premier:
                    self.stats["firsts"][joueur["pseudo"]] = (
                        self.stats["firsts"].get(joueur["pseudo"], 0) + 1)
            await self.diffuser({"type": "essai", "pseudo": joueur["pseudo"],
                                 "bon": True})
            await self.envoyer(joueur, {"type": "trouve", "points": 0,
                                        "premier": premier, "double": False})
            await self.diffuser({
                "type": "quelquun_a_trouve", "pseudo": joueur["pseudo"],
                "premier": premier,
                "fin_dans": max(0, round(self.fin_prevue - time.time())),
                "joueurs": self.liste_joueurs(),
            })
            return

        ecoule = time.time() - self.debut
        gagnes = points_pour(ecoule, self.duree_courante)
        premier = self.premier is None
        if premier:
            self.premier = jeton
            gagnes += BONUS_PREMIER
            # La manche se termine plus tard, sans depasser la duree prevue.
            self.fin_prevue = min(time.time() + self.fenetre_effective(),
                                  self.debut + self.duree_courante)

        # Pouvoir "double ou rien" arme : points de la manche doubles.
        double = joueur.get("double_arme")
        if double:
            gagnes *= 2
            joueur["double_arme"] = False

        joueur["score"] += gagnes
        joueur["trouve"] = True

        # Serie de bonnes reponses -> charges de pouvoir (mode "pouvoirs" seul).
        if self.mode == "pouvoirs":
            joueur["serie"] = joueur.get("serie", 0) + 1
            if joueur["serie"] % SERIE_POUR_CHARGE == 0:
                joueur["charges"] = min(3, joueur.get("charges", 0) + 1)
                await self.envoyer(joueur, {"type": "charge_gagnee",
                                            "charges": joueur["charges"]})

        # Stats de la partie (podium + faits rigolos).
        if self.stats is not None:
            if (self.stats["rapide_temps"] is None
                    or ecoule < self.stats["rapide_temps"]):
                self.stats["rapide_temps"] = ecoule
                self.stats["rapide_pseudo"] = joueur["pseudo"]
            if premier:
                self.stats["firsts"][joueur["pseudo"]] = (
                    self.stats["firsts"].get(joueur["pseudo"], 0) + 1)

        # Bonne reponse : on l'annonce dans le fil SANS reveler le mot.
        await self.diffuser({
            "type": "essai",
            "pseudo": joueur["pseudo"],
            "bon": True,
        })

        await self.envoyer(joueur, {
            "type": "trouve", "points": gagnes, "premier": premier,
            "double": double})
        await self.diffuser({
            "type": "quelquun_a_trouve",
            "pseudo": joueur["pseudo"],
            "premier": premier,
            "fin_dans": max(0, round(self.fin_prevue - time.time())),
            "joueurs": self.liste_joueurs(),
        })

    async def utiliser_pouvoir(self, jeton, pouvoir, cible=None):
        """Depense 1 charge pour declencher un pouvoir (conditions: manche en
        cours, joueur en jeu qui n'a pas encore trouve, charge dispo, recharge
        ecoulee)."""
        if self.mode != "pouvoirs":
            return                          # pouvoirs reserves au mode dedie
        if self.etat != "manche" or pouvoir not in POUVOIRS:
            return
        j = self.joueurs.get(jeton)
        if not j or j.get("trouve") or not self.en_jeu(j) or j["ws"] is None:
            return
        if self.repondeurs is not None and jeton not in self.repondeurs:
            return                          # pouvoir reserve aux repondeurs actifs
        maintenant = time.time()
        if j.get("charges", 0) < 1 or maintenant < j.get("cooldown", 0):
            await self.envoyer(j, {"type": "pouvoir_refuse"})
            return

        if pouvoir == "indice":
            await self.envoyer(j, {"type": "indice",
                                   "indice": indice_de(self.question["reponse"])})
        elif pouvoir == "gel":
            for k, autre in self.joueurs.items():
                if (k != jeton and autre["ws"] is not None
                        and self.en_jeu(autre) and not autre.get("trouve")):
                    autre["gel_jusqua"] = maintenant + DUREE_GEL
                    await self.envoyer(autre, {"type": "gele_debut",
                                               "duree": DUREE_GEL,
                                               "par": j["pseudo"]})
        elif pouvoir == "double":
            j["double_arme"] = True
        elif pouvoir == "skip":
            # Passe la manche sans penalite : compte comme "traite" (protege
            # d'une perte de vie en survie) mais ne rapporte aucun point.
            j["trouve"] = True

        j["charges"] = j.get("charges", 0) - 1
        j["cooldown"] = maintenant + COOLDOWN_POUVOIR
        await self.envoyer(j, {"type": "pouvoir_ok", "pouvoir": pouvoir,
                               "charges": j["charges"]})
        # Petit avis public que quelqu'un a joue un pouvoir (ambiance).
        await self.diffuser({"type": "pouvoir_joue",
                             "pseudo": j["pseudo"], "pouvoir": pouvoir})


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
                        "pseudo": pseudo, "score": 0, "ws": ws,
                        "trouve": False, "equipe": None}
                    if salon.equipes:
                        salon.equilibrer()
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
                if "duree" in message:
                    try:
                        salon.duree = max(10, min(40, int(message["duree"])))
                    except (TypeError, ValueError):
                        pass
                if "objectif" in message:
                    try:
                        salon.objectif = max(20, min(300, int(message["objectif"])))
                    except (TypeError, ValueError):
                        pass
                if "manches_max" in message:
                    try:
                        salon.manches_max = max(0, min(50, int(message["manches_max"])))
                    except (TypeError, ValueError):
                        pass
                await salon.diffuser_etat()

            elif action == "mode" and jeton == salon.hote:
                m = message.get("mode")
                if m in MODES and salon.etat in ("salon", "fini"):
                    salon.mode = m
                    salon.equipes = (m == "equipes")
                    if salon.equipes:
                        salon.equilibrer()
                    await salon.diffuser_etat()

            elif action == "pouvoir":
                await salon.utiliser_pouvoir(jeton, message.get("pouvoir"),
                                             message.get("cible"))

            elif action == "choisir_equipe":
                e = message.get("equipe")
                if e in ("A", "B") and jeton in salon.joueurs:
                    salon.joueurs[jeton]["equipe"] = e
                    await salon.diffuser_etat()

            elif action == "demarrer":
                # N'importe quel joueur peut (re)lancer : le gagnant n'est pas
                # forcement l'hote. Verrou pour eviter un double-lancement.
                if (salon.etat in ("salon", "fini")
                        and (salon.boucle is None or salon.boucle.done())):
                    for j in salon.joueurs.values():
                        j["score"] = 0
                        j["trouve"] = False
                        j["vies"] = VIES_SURVIE
                        j["elimine"] = False
                        j["charges"] = 0
                        j["serie"] = 0
                        j["cooldown"] = 0
                        j["gel_jusqua"] = 0
                        j["double_arme"] = False
                        j["match"] = 0
                    salon.deja_posees = []
                    salon.numero = 0
                    salon.repondeurs = None
                    salon.etat = "manche"   # verrou synchrone anti double-lancement
                    if salon.mode == "tournoi":
                        salon.boucle = asyncio.create_task(salon.jouer_tournoi())
                    elif salon.mode == "bombe":
                        salon.boucle = asyncio.create_task(salon.jouer_bombe())
                    elif salon.mode == "quittedouble":
                        salon.boucle = asyncio.create_task(salon.jouer_quittedouble())
                    else:
                        salon.boucle = asyncio.create_task(salon.jouer())

            elif action == "miser":
                if (salon.mode == "quittedouble" and salon.phase_mise
                        and jeton in salon.joueurs):
                    try:
                        salon.mises[jeton] = max(0, int(message.get("mise", 0)))
                    except (TypeError, ValueError):
                        pass

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
