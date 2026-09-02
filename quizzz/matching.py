"""
Normalisation et validation des reponses tapees.
"""

import re
import unicodedata

ARTICLES = {
    "le", "la", "les", "l", "un", "une", "des", "du", "de", "d",
    "the", "a", "an", "el", "los", "las",
}

PREFIXES_PARASITES = [
    "c est", "cest", "je pense que c est", "je crois que c est",
    "la reponse est", "reponse", "peut etre",
]


def enlever_accents(texte: str) -> str:
    nfkd = unicodedata.normalize("NFKD", texte)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normaliser(texte: str) -> str:
    if not texte:
        return ""

    texte = enlever_accents(texte.lower())
    texte = re.sub(r"['\u2019`]", " ", texte)
    texte = re.sub(r"[^a-z0-9 ]", " ", texte)
    texte = re.sub(r"\s+", " ", texte).strip()

    for prefixe in PREFIXES_PARASITES:
        if texte.startswith(prefixe + " "):
            texte = texte[len(prefixe) + 1:]

    mots = texte.split()
    while mots and mots[0] in ARTICLES:
        mots.pop(0)

    return " ".join(mots)


def levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    ligne_precedente = list(range(len(b) + 1))
    for i, car_a in enumerate(a):
        ligne_courante = [i + 1]
        for j, car_b in enumerate(b):
            insertion = ligne_precedente[j + 1] + 1
            suppression = ligne_courante[j] + 1
            substitution = ligne_precedente[j] + (car_a != car_b)
            ligne_courante.append(min(insertion, suppression, substitution))
        ligne_precedente = ligne_courante

    return ligne_precedente[-1]


def tolerance_fautes(reponse_normalisee: str) -> int:
    n = len(reponse_normalisee)
    if n <= 4:
        return 0
    if n <= 8:
        return 1
    if n <= 15:
        return 2
    return 3


def verifier_reponse(saisie: str, reponse: str, alias=None) -> bool:
    saisie_norm = normaliser(saisie)
    if not saisie_norm:
        return False

    candidats = [reponse] + list(alias or [])

    for candidat in candidats:
        candidat_norm = normaliser(candidat)
        if not candidat_norm:
            continue
        if saisie_norm == candidat_norm:
            return True
        if levenshtein(saisie_norm, candidat_norm) <= tolerance_fautes(candidat_norm):
            return True

    return False


if __name__ == "__main__":
    cas = [
        ("leonard de vinci", "Léonard de Vinci", [], True),
        ("LEONARD DE VINCI", "Léonard de Vinci", [], True),
        ("leonrad de vinci", "Léonard de Vinci", [], True),
        ("de vinci", "Léonard de Vinci", ["de Vinci", "Vinci"], True),
        ("vinci", "Léonard de Vinci", ["de Vinci", "Vinci"], True),
        ("michel ange", "Léonard de Vinci", ["de Vinci"], False),
        ("bejaia", "Béjaïa", [], True),
        ("l'algerie", "Algérie", [], True),
        ("c'est paris", "Paris", [], True),
        ("ross", "Rome", [], False),
        ("les fennecs", "Équipe d'Algérie de football", ["Fennecs", "Algérie"], True),
        ("", "Paris", [], False),
    ]

    echecs = 0
    for saisie, reponse, alias, attendu in cas:
        obtenu = verifier_reponse(saisie, reponse, alias)
        statut = "OK " if obtenu == attendu else "ECHEC"
        if obtenu != attendu:
            echecs += 1
        print(f"{statut} | {saisie!r:35} vs {reponse!r:35} -> {obtenu}")

    print(f"\n{len(cas) - echecs}/{len(cas)} tests passes.")