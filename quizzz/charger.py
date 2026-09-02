"""
Charge un fichier de questions JSON dans la banque.
Aucun appel API, aucun cout.
"""

import argparse
import json
import sqlite3
import sys

from matching import normaliser

BASE = "questions.db"
DIFFICULTES = ["facile", "moyen", "difficile"]
CATEGORIES = ["algerie", "football", "nba", "sport", "anime",
              "film", "series", "culture_g", "geographie", "histoire", "physique"]


def ouvrir_base():
    conn = sqlite3.connect(BASE)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS questions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            question    TEXT NOT NULL,
            cle         TEXT NOT NULL UNIQUE,
            reponse     TEXT NOT NULL,
            alias       TEXT NOT NULL,
            categorie   TEXT NOT NULL,
            difficulte  TEXT NOT NULL,
            avec_image  INTEGER NOT NULL DEFAULT 0,
            sujet_image TEXT DEFAULT '',
            url_image   TEXT DEFAULT '',
            image_ok    INTEGER NOT NULL DEFAULT 0,
            signalements INTEGER NOT NULL DEFAULT 0
        );
        CREATE INDEX IF NOT EXISTS idx_cat ON questions(categorie, difficulte);
    """)
    conn.commit()
    return conn


def charger(chemin):
    try:
        with open(chemin, encoding="utf-8") as f:
            lot = json.load(f)
    except FileNotFoundError:
        sys.exit(f"Fichier introuvable : {chemin}")
    except json.JSONDecodeError as e:
        sys.exit(f"Le fichier JSON est mal forme : {e}\n"
                 f"Verifie qu'il n'y a pas de virgule en trop a la fin.")

    if not isinstance(lot, list):
        sys.exit("Le fichier doit contenir une liste de questions.")

    conn = ouvrir_base()
    ajoutees = doublons = invalides = 0

    for q in lot:
        if not isinstance(q, dict):
            invalides += 1
            continue
        question = (q.get("question") or "").strip()
        reponse = (q.get("reponse") or "").strip()
        categorie = (q.get("categorie") or "").strip()
        difficulte = (q.get("difficulte") or "moyen").strip()

        if not question or not reponse:
            invalides += 1
            continue
        if categorie not in CATEGORIES:
            print(f"  ! categorie inconnue '{categorie}' : {question[:50]}")
            invalides += 1
            continue
        if difficulte not in DIFFICULTES:
            difficulte = "moyen"

        alias = [a for a in (q.get("alias") or []) if isinstance(a, str)]

        url_image = (q.get("url_image") or q.get("image") or "").strip()
        sujet_image = (q.get("sujet_image") or "").strip()
        avec_image = 1 if url_image else 0

        # Les questions a image partagent souvent le meme texte
        # ("Quel pays a ce drapeau ?") : on distingue par l'image.
        cle = normaliser(question)
        if url_image:
            cle = cle + "|" + url_image

        try:
            conn.execute(
                "INSERT INTO questions (question, cle, reponse, alias, "
                "categorie, difficulte, avec_image, url_image, sujet_image) "
                "VALUES (?,?,?,?,?,?,?,?,?)",
                (question, cle, reponse,
                 json.dumps(alias, ensure_ascii=False), categorie, difficulte,
                 avec_image, url_image, sujet_image),
            )
            ajoutees += 1
        except sqlite3.IntegrityError:
            doublons += 1

    conn.commit()
    print(f"\n{ajoutees} ajoutees, {doublons} doublons ignores, "
          f"{invalides} invalides.")
    conn.close()


def stats():
    conn = ouvrir_base()
    total = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
    print(f"\nBanque : {total} questions\n")
    entete = "  ".join(f"{d:>10}" for d in DIFFICULTES)
    print(f"{'categorie':13} {entete}      total")
    for cat in CATEGORIES:
        vals = []
        for d in DIFFICULTES:
            n = conn.execute(
                "SELECT COUNT(*) FROM questions WHERE categorie=? AND difficulte=?",
                (cat, d)).fetchone()[0]
            vals.append(n)
        ligne = "  ".join(f"{v:>10}" for v in vals)
        print(f"{cat:13} {ligne} {sum(vals):>10}")
    conn.close()


def apercu(n=8):
    conn = ouvrir_base()
    rows = conn.execute(
        "SELECT question, categorie, difficulte FROM questions "
        "ORDER BY RANDOM() LIMIT ?", (n,)).fetchall()
    if not rows:
        print("\nLa banque est vide.")
        return
    print("\nApercu (reponses masquees) :\n")
    for q, c, d in rows:
        print(f"  ({c}/{d}) {q}")
    conn.close()


def tester():
    from matching import verifier_reponse
    conn = ouvrir_base()
    row = conn.execute(
        "SELECT question, reponse, alias FROM questions "
        "ORDER BY RANDOM() LIMIT 1").fetchone()
    if not row:
        print("La banque est vide.")
        return
    question, reponse, alias = row
    print(f"\n{question}")
    saisie = input("> ")
    if verifier_reponse(saisie, reponse, json.loads(alias)):
        print("CORRECT")
    else:
        print(f"FAUX. Reponse attendue : {reponse}")
    conn.close()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("fichier", nargs="?", help="fichier JSON a charger")
    p.add_argument("--stats", action="store_true")
    p.add_argument("--apercu", action="store_true")
    p.add_argument("--tester", action="store_true")
    args = p.parse_args()

    if args.stats:
        stats()
    elif args.apercu:
        apercu()
    elif args.tester:
        tester()
    elif args.fichier:
        charger(args.fichier)
        stats()
    else:
        p.print_help()