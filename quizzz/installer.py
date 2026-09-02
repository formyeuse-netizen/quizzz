import base64, zlib, json, hashlib
CIBLES = {"p1.txt": "8e078af7", "p2.txt": "df2ec81b", "p3.txt": "75c8c7a9"}
morceaux, ok = [], True
for nom in CIBLES:
    txt = "".join(open(nom, encoding="utf-8").read().split())
    vu = hashlib.md5(txt.encode()).hexdigest()[:8]
    bon = vu == CIBLES[nom]
    ok = ok and bon
    print(nom, len(txt), "caracteres", "OK" if bon else "FAUX (attendu " + CIBLES[nom] + ", trouve " + vu + ")")
if not ok:
    raise SystemExit("Une partie est abimee. Signale laquelle.")
fichiers = json.loads(zlib.decompress(base64.b64decode("".join(morceaux) or "".join("".join(open(n, encoding="utf-8").read().split()) for n in CIBLES))).decode("utf-8"))
for nom in fichiers:
    open(nom, "w", encoding="utf-8").write(fichiers[nom])
    print("ecrit :", nom, "-", len(fichiers[nom]), "caracteres")