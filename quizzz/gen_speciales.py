# -*- coding: utf-8 -*-
"""
Genere lot_speciales.json : questions "Citez-en un" (plusieurs bonnes
reponses, chacune ne peut etre prise qu'une fois) et "Lequel est le plus…"
(duel entre 2 propositions, un seul essai).

    py gen_speciales.py      puis      py charger.py lot_speciales.json
"""
import itertools
import json
import random
import unicodedata

from pays_data import PAYS

random.seed(2026)
OUT = []


def sans_accent(t):
    return "".join(c for c in unicodedata.normalize("NFKD", t)
                   if not unicodedata.combining(c))


def citez(question, categorie, difficulte, groupes):
    """groupes : liste de reponses ; chaque reponse = str ou liste d'alias."""
    gs = []
    for g in groupes:
        g = [g] if isinstance(g, str) else list(g)
        gs.append(g)
    exemples = ", ".join(g[0] for g in gs[:6]) + ("…" if len(gs) > 6 else "")
    OUT.append({
        "type": "citez", "question": question, "categorie": categorie,
        "difficulte": difficulte,
        "reponse": f"{exemples} ({len(gs)} réponses possibles)",
        "alias": [], "extra": {"groupes": gs},
    })


def duel(question, categorie, difficulte, bonne, mauvaise):
    b = [bonne] if isinstance(bonne, str) else list(bonne)
    m = [mauvaise] if isinstance(mauvaise, str) else list(mauvaise)
    options = [b, m]
    random.shuffle(options)
    OUT.append({
        "type": "duel", "question": question, "categorie": categorie,
        "difficulte": difficulte, "reponse": b[0], "alias": b[1:],
        "extra": {"options": options, "bonne": options.index(b)},
    })


# ---------------------------------------------------------------------------
# PAYS (depuis pays_data.py)
# ---------------------------------------------------------------------------
P = {code: (nom, cap, al, alc) for code, nom, cap, dif, al, alc in PAYS}


def gp(code):
    nom, cap, al, alc = P[code]
    return [nom] + al


def gc(code):
    nom, cap, al, alc = P[code]
    return [cap] + alc


src = open("pays_data.py", encoding="utf-8").read().splitlines()
continent, CONT = None, {}
for ligne in src:
    if "# ----" in ligne:
        for k in ("AFRIQUE", "ASIE", "EUROPE", "AMÉRIQUES", "OCÉANIE"):
            if k in ligne:
                continent = k
    elif ligne.strip().startswith('("') and continent:
        code = ligne.strip()[2:4]
        CONT.setdefault(continent, []).append(code)

AMSUD = ["ar", "bo", "br", "cl", "co", "ec", "gy", "py", "pe", "sr", "uy", "ve"]
AMCENT = ["bz", "cr", "sv", "gt", "hn", "ni", "pa"]
AMS = [c for c in CONT["AMÉRIQUES"]]

citez("Citez un pays d'Afrique", "geographie", "facile", [gp(c) for c in CONT["AFRIQUE"]])
citez("Citez un pays d'Asie", "geographie", "facile", [gp(c) for c in CONT["ASIE"]])
citez("Citez un pays d'Europe", "geographie", "facile", [gp(c) for c in CONT["EUROPE"]])
citez("Citez un pays d'Amérique du Sud", "geographie", "facile",
      [gp(c) for c in AMSUD if c in P])
citez("Citez un pays d'Amérique centrale", "geographie", "moyen",
      [gp(c) for c in AMCENT if c in P])
citez("Citez un pays d'Océanie", "geographie", "moyen", [gp(c) for c in CONT["OCÉANIE"]])
citez("Citez une capitale africaine", "geographie", "moyen", [gc(c) for c in CONT["AFRIQUE"]])
citez("Citez une capitale européenne", "geographie", "facile", [gc(c) for c in CONT["EUROPE"]])
citez("Citez une capitale asiatique", "geographie", "moyen", [gc(c) for c in CONT["ASIE"]])
citez("Citez une capitale d'Amérique (Nord, Centre ou Sud)", "geographie", "moyen",
      [gc(c) for c in AMS])

# Pays par premiere lettre (seulement les alias qui commencent par la meme lettre)
par_lettre = {}
for code, (nom, cap, al, alc) in P.items():
    L = sans_accent(nom)[0].upper()
    par_lettre.setdefault(L, []).append(
        [nom] + [a for a in al if sans_accent(a)[0].upper() == L])
for L, gs in sorted(par_lettre.items()):
    if len(gs) >= 7:
        dif = "facile" if len(gs) >= 12 else "moyen"
        citez(f"Citez un pays dont le nom (en français) commence par la lettre {L}",
              "geographie", dif, gs)

citez("Citez un pays qui a une frontière avec l'Algérie", "algerie", "facile",
      [gp("tn"), gp("ly"), gp("ne"), gp("ml"), gp("mr"), gp("ma"),
       ["Sahara occidental", "Western Sahara", "Sahara"]])
citez("Citez un pays qui a une frontière terrestre avec la France métropolitaine",
      "geographie", "moyen",
      [gp("be"), gp("lu"), gp("de"), gp("ch"), gp("it"), gp("mc"), gp("es"), gp("ad")])
citez("Citez un pays du Maghreb", "geographie", "facile",
      [gp("dz"), gp("ma"), gp("tn"), gp("ly"), gp("mr")])
citez("Citez un pays membre de la Ligue arabe", "geographie", "moyen",
      [gp(c) for c in ["dz", "sa", "bh", "km", "dj", "eg", "ae", "iq", "jo", "kw", "lb",
                       "ly", "ma", "mr", "om", "ps", "qa", "so", "sd", "sy", "tn", "ye"]])
citez("Citez un pays membre de l'Union européenne", "geographie", "facile",
      [gp(c) for c in ["de", "at", "be", "bg", "cy", "hr", "dk", "es", "ee", "fi", "fr",
                       "gr", "hu", "ie", "it", "lv", "lt", "lu", "mt", "nl", "pl", "pt",
                       "cz", "ro", "sk", "si", "se"]])
citez("Citez un pays où l'on paie en euros", "geographie", "moyen",
      [gp(c) for c in ["de", "at", "be", "bg", "cy", "hr", "es", "ee", "fi", "fr", "gr",
                       "ie", "it", "lv", "lt", "lu", "mt", "nl", "pt", "sk", "si",
                       "mc", "va", "sm", "ad", "me", "xk"] if c in P])
citez("Citez un pays membre du G7", "geographie", "moyen",
      [gp(c) for c in ["us", "ca", "fr", "de", "it", "jp", "gb"]])
citez("Citez un pays traversé par l'équateur", "geographie", "difficile",
      [gp(c) for c in ["ec", "co", "br", "ga", "cg", "cd", "ug", "ke", "so", "id",
                       "mv", "ki", "st"]])
citez("Citez un pays d'Afrique sans accès à la mer", "geographie", "difficile",
      [gp(c) for c in ["bf", "bi", "cf", "td", "et", "ls", "mw", "ml", "ne", "rw",
                       "ss", "ug", "zm", "zw", "bw", "sz"]])
citez("Citez un pays où l'espagnol est langue officielle", "geographie", "moyen",
      [gp(c) for c in ["es", "mx", "co", "ar", "pe", "ve", "cl", "ec", "gt", "cu", "bo",
                       "do", "hn", "py", "sv", "ni", "cr", "pa", "uy", "gq"]])
citez("Citez un pays où le portugais est langue officielle", "geographie", "moyen",
      [gp(c) for c in ["pt", "br", "ao", "mz", "cv", "gw", "st", "tl", "gq"]])
citez("Citez un pays d'Afrique où le français est langue officielle", "geographie",
      "moyen", [gp(c) for c in ["bj", "bf", "bi", "cm", "cf", "km", "cg", "cd", "ci",
                                "dj", "ga", "gn", "gq", "mg", "ml", "ne", "rw", "sn",
                                "sc", "td", "tg"]])

# ---------------------------------------------------------------------------
# FOOTBALL / SPORT
# ---------------------------------------------------------------------------
citez("Citez un pays qui a déjà gagné la Coupe du monde de football", "football", "facile",
      [gp("br"), gp("de"), gp("it"), gp("ar"), gp("fr"), gp("uy"),
       ["Angleterre", "England"], gp("es")])
citez("Citez un pays qui a déjà organisé la Coupe du monde de football", "football",
      "moyen",
      [gp("uy"), gp("it"), gp("fr"), gp("br"), gp("ch"), gp("se"), gp("cl"),
       ["Angleterre", "England"], gp("mx"), gp("de"), gp("ar"), gp("es"), gp("us"),
       gp("kr"), gp("jp"), gp("za"), gp("ru"), gp("qa"), gp("ca")])
citez("Citez un pays qui a gagné l'Euro de football", "football", "moyen",
      [gp("de"), gp("es"), gp("fr"), gp("it"), ["URSS", "Union soviétique", "USSR"],
       ["Tchécoslovaquie", "Czechoslovakia"], gp("nl"), gp("dk"), gp("gr"), gp("pt")])
citez("Citez un pays qui a gagné la Coupe d'Afrique des nations", "football", "moyen",
      [gp("eg"), gp("cm"), gp("gh"), gp("ng"), gp("ci"), gp("dz"), gp("cd"), gp("zm"),
       gp("tn"), gp("za"), gp("ma"), gp("sd"), gp("et"), gp("cg"), gp("sn")])
citez("Citez un club qui a gagné la Ligue des champions (jusqu'en 2025)", "football",
      "moyen",
      [["Real Madrid", "Real"], ["AC Milan", "Milan"], ["Bayern Munich", "Bayern"],
       ["Liverpool"], ["FC Barcelone", "Barcelone", "Barça", "Barcelona"], ["Ajax", "Ajax Amsterdam"],
       ["Inter Milan", "Inter"], ["Manchester United", "Man United", "Man U"],
       ["Juventus", "Juve"], ["Benfica"], ["Chelsea"], ["FC Porto", "Porto"],
       ["Nottingham Forest", "Nottingham"], ["Borussia Dortmund", "Dortmund"],
       ["Celtic", "Celtic Glasgow"], ["Hambourg", "Hamburg", "Hambourg SV"],
       ["Steaua Bucarest", "Steaua"], ["Olympique de Marseille", "Marseille", "OM"],
       ["Feyenoord"], ["Aston Villa"], ["PSV Eindhoven", "PSV"],
       ["Étoile rouge de Belgrade", "Etoile rouge", "Red Star Belgrade", "Crvena Zvezda"],
       ["Manchester City", "Man City", "City"], ["Paris Saint-Germain", "PSG", "Paris"]])
citez("Citez un joueur qui a gagné le Ballon d'Or", "football", "moyen",
      [["Stanley Matthews", "Matthews"], ["Alfredo Di Stéfano", "Di Stefano"],
       ["Raymond Kopa", "Kopa"], ["Luis Suárez (1960)", "Luis Suarez", "Suarez"],
       ["Omar Sívori", "Sivori"], ["Josef Masopust", "Masopust"],
       ["Lev Yachine", "Yachine", "Yashin"], ["Denis Law"], ["Eusébio", "Eusebio"],
       ["Bobby Charlton", "Charlton"], ["Flórián Albert", "Florian Albert"],
       ["George Best", "Best"], ["Gianni Rivera", "Rivera"], ["Gerd Müller", "Muller", "Gerd Muller"],
       ["Johan Cruyff", "Cruyff"], ["Franz Beckenbauer", "Beckenbauer"],
       ["Oleg Blokhine", "Blokhine", "Blokhin"], ["Allan Simonsen", "Simonsen"],
       ["Kevin Keegan", "Keegan"], ["Karl-Heinz Rummenigge", "Rummenigge"],
       ["Paolo Rossi"], ["Michel Platini", "Platini"], ["Igor Belanov", "Belanov"],
       ["Ruud Gullit", "Gullit"], ["Marco van Basten", "Van Basten"],
       ["Lothar Matthäus", "Matthaus", "Matthäus"], ["Jean-Pierre Papin", "Papin", "JPP"],
       ["Roberto Baggio", "Baggio"], ["Hristo Stoitchkov", "Stoitchkov", "Stoichkov"],
       ["George Weah", "Weah"], ["Matthias Sammer", "Sammer"],
       ["Ronaldo (R9)", "Ronaldo", "R9", "Ronaldo Nazario"],
       ["Zinédine Zidane", "Zidane", "Zizou"], ["Rivaldo"], ["Luís Figo", "Figo"],
       ["Michael Owen", "Owen"], ["Pavel Nedvěd", "Nedved"],
       ["Andriy Shevchenko", "Shevchenko", "Chevtchenko"],
       ["Ronaldinho"], ["Fabio Cannavaro", "Cannavaro"], ["Kaká", "Kaka"],
       ["Cristiano Ronaldo", "CR7", "Cristiano"], ["Lionel Messi", "Messi"],
       ["Luka Modrić", "Modric"], ["Karim Benzema", "Benzema"], ["Rodri"],
       ["Ousmane Dembélé", "Dembele"], ["Harry Kane", "Kane"]])
citez("Citez un joueur de l'équipe de France championne du monde 2018", "football",
      "difficile",
      [["Hugo Lloris", "Lloris"], ["Steve Mandanda", "Mandanda"], ["Alphonse Areola", "Areola"],
       ["Benjamin Pavard", "Pavard"], ["Raphaël Varane", "Varane"], ["Samuel Umtiti", "Umtiti"],
       ["Lucas Hernandez", "Hernandez"], ["Presnel Kimpembe", "Kimpembe"],
       ["Benjamin Mendy", "Mendy"], ["Djibril Sidibé", "Sidibe"], ["Adil Rami", "Rami"],
       ["N'Golo Kanté", "Kante"], ["Paul Pogba", "Pogba"], ["Blaise Matuidi", "Matuidi"],
       ["Corentin Tolisso", "Tolisso"], ["Steven N'Zonzi", "Nzonzi"],
       ["Antoine Griezmann", "Griezmann"], ["Kylian Mbappé", "Mbappe"],
       ["Olivier Giroud", "Giroud"], ["Ousmane Dembélé", "Dembele"],
       ["Thomas Lemar", "Lemar"], ["Florian Thauvin", "Thauvin"], ["Nabil Fekir", "Fekir"]])
citez("Citez une équipe de NBA", "nba", "facile",
      [["Atlanta Hawks", "Hawks"], ["Boston Celtics", "Celtics"], ["Brooklyn Nets", "Nets"],
       ["Charlotte Hornets", "Hornets"], ["Chicago Bulls", "Bulls"],
       ["Cleveland Cavaliers", "Cavaliers", "Cavs"], ["Dallas Mavericks", "Mavericks", "Mavs"],
       ["Denver Nuggets", "Nuggets"], ["Detroit Pistons", "Pistons"],
       ["Golden State Warriors", "Warriors", "Golden State"], ["Houston Rockets", "Rockets"],
       ["Indiana Pacers", "Pacers"], ["Los Angeles Clippers", "Clippers"],
       ["Los Angeles Lakers", "Lakers"], ["Memphis Grizzlies", "Grizzlies"],
       ["Miami Heat", "Heat"], ["Milwaukee Bucks", "Bucks"],
       ["Minnesota Timberwolves", "Timberwolves", "Wolves"],
       ["New Orleans Pelicans", "Pelicans"], ["New York Knicks", "Knicks"],
       ["Oklahoma City Thunder", "Thunder", "OKC"], ["Orlando Magic", "Magic"],
       ["Philadelphia 76ers", "76ers", "Sixers"], ["Phoenix Suns", "Suns"],
       ["Portland Trail Blazers", "Trail Blazers", "Blazers"],
       ["Sacramento Kings", "Kings"], ["San Antonio Spurs", "Spurs"],
       ["Toronto Raptors", "Raptors"], ["Utah Jazz", "Jazz"],
       ["Washington Wizards", "Wizards"]])
citez("Citez un pilote champion du monde de Formule 1", "sport", "moyen",
      [["Giuseppe Farina", "Farina"], ["Juan Manuel Fangio", "Fangio"],
       ["Alberto Ascari", "Ascari"], ["Mike Hawthorn", "Hawthorn"],
       ["Jack Brabham", "Brabham"], ["Phil Hill", "Graham Hill", "Damon Hill", "Hill"],
       ["Jim Clark", "Clark"], ["John Surtees", "Surtees"], ["Denny Hulme", "Hulme"],
       ["Jackie Stewart", "Stewart"], ["Jochen Rindt", "Rindt"],
       ["Emerson Fittipaldi", "Fittipaldi"], ["Niki Lauda", "Lauda"],
       ["James Hunt", "Hunt"], ["Mario Andretti", "Andretti"],
       ["Jody Scheckter", "Scheckter"], ["Alan Jones"], ["Nelson Piquet", "Piquet"],
       ["Keke Rosberg", "Nico Rosberg", "Rosberg"], ["Alain Prost", "Prost"],
       ["Ayrton Senna", "Senna"], ["Nigel Mansell", "Mansell"],
       ["Michael Schumacher", "Schumacher"], ["Jacques Villeneuve", "Villeneuve"],
       ["Mika Häkkinen", "Hakkinen"], ["Fernando Alonso", "Alonso"],
       ["Kimi Räikkönen", "Raikkonen"], ["Lewis Hamilton", "Hamilton"],
       ["Jenson Button", "Button"], ["Sebastian Vettel", "Vettel"],
       ["Max Verstappen", "Verstappen"], ["Lando Norris", "Norris"]])
citez("Citez une ville qui a accueilli les Jeux olympiques d'été", "sport", "moyen",
      ["Athènes", ["Paris"], ["Saint-Louis", "St Louis", "Saint Louis"], ["Londres", "London"],
       ["Stockholm"], ["Anvers", "Antwerp"], ["Amsterdam"], ["Los Angeles", "LA"],
       ["Berlin"], ["Helsinki"], ["Melbourne"], ["Rome", "Roma"], ["Tokyo"],
       ["Mexico"], ["Munich", "München"], ["Montréal", "Montreal"],
       ["Moscou", "Moscow"], ["Séoul", "Seoul"], ["Barcelone", "Barcelona"],
       ["Atlanta"], ["Sydney"], ["Pékin", "Pekin", "Beijing"],
       ["Rio de Janeiro", "Rio"]])
citez("Citez un sport des Jeux olympiques d'hiver", "sport", "facile",
      [["Ski alpin", "ski"], ["Ski de fond"], ["Saut à ski", "saut a ski"], ["Biathlon"],
       ["Combiné nordique"], ["Snowboard"], ["Ski acrobatique", "freestyle", "ski freestyle"],
       ["Patinage artistique"], ["Patinage de vitesse", "patinage"], ["Short-track", "short track"],
       ["Hockey sur glace", "hockey"], ["Curling"], ["Bobsleigh", "bobsled", "bob"],
       ["Luge"], ["Skeleton"], ["Ski-alpinisme", "ski alpinisme"]])
citez("Citez un tournoi du Grand Chelem de tennis", "sport", "facile",
      [["Open d'Australie", "Australian Open", "Melbourne"],
       ["Roland-Garros", "Roland Garros", "French Open"],
       ["Wimbledon"], ["US Open", "Flushing Meadows"]])

# ---------------------------------------------------------------------------
# FILMS / SERIES / ANIME / JEUX
# ---------------------------------------------------------------------------
citez("Citez un film des studios Pixar", "film", "moyen",
      [["Toy Story"], ["1001 pattes", "Mille et une pattes", "A Bug's Life"],
       ["Toy Story 2"], ["Monstres & Cie", "Monstres et Cie", "Monsters Inc"],
       ["Le Monde de Nemo", "Nemo", "Finding Nemo"],
       ["Les Indestructibles", "The Incredibles"], ["Cars"], ["Ratatouille"],
       ["WALL-E", "Wall E"], ["Là-haut", "La haut", "Up"], ["Toy Story 3"],
       ["Cars 2"], ["Rebelle", "Brave"], ["Monstres Academy", "Monsters University"],
       ["Vice-versa", "Vice versa", "Inside Out"], ["Le Voyage d'Arlo", "Arlo", "The Good Dinosaur"],
       ["Le Monde de Dory", "Dory", "Finding Dory"], ["Cars 3"], ["Coco"],
       ["Les Indestructibles 2", "Incredibles 2"], ["Toy Story 4"],
       ["En avant", "Onward"], ["Soul"], ["Luca"], ["Alerte rouge", "Turning Red"],
       ["Buzz l'Éclair", "Lightyear", "Buzz l'Eclair"], ["Élémentaire", "Elemental", "Elementaire"],
       ["Vice-versa 2", "Inside Out 2"], ["Elio"]])
citez("Citez un film de Christopher Nolan", "film", "moyen",
      [["Following"], ["Memento"], ["Insomnia"], ["Batman Begins"],
       ["Le Prestige", "The Prestige"], ["The Dark Knight"], ["Inception"],
       ["The Dark Knight Rises"], ["Interstellar"], ["Dunkerque", "Dunkirk"],
       ["Tenet"], ["Oppenheimer"], ["L'Odyssée", "The Odyssey", "Odyssée"]])
citez("Citez un film de Quentin Tarantino", "film", "moyen",
      [["Reservoir Dogs"], ["Pulp Fiction"], ["Jackie Brown"], ["Kill Bill"],
       ["Boulevard de la mort", "Death Proof"], ["Inglourious Basterds"],
       ["Django Unchained", "Django"], ["Les Huit Salopards", "The Hateful Eight", "Hateful Eight"],
       ["Once Upon a Time in Hollywood", "Il était une fois à Hollywood"]])
citez("Citez un film d'Hayao Miyazaki", "anime", "moyen",
      [["Le Château de Cagliostro", "Cagliostro"], ["Nausicaä de la vallée du vent", "Nausicaa"],
       ["Le Château dans le ciel", "Laputa", "Castle in the Sky"],
       ["Mon voisin Totoro", "Totoro", "My Neighbor Totoro"],
       ["Kiki la petite sorcière", "Kiki"], ["Porco Rosso"],
       ["Princesse Mononoké", "Mononoke"], ["Le Voyage de Chihiro", "Chihiro", "Spirited Away"],
       ["Le Château ambulant", "Howl's Moving Castle", "Chateau ambulant"],
       ["Ponyo sur la falaise", "Ponyo"], ["Le vent se lève", "The Wind Rises"],
       ["Le Garçon et le Héron", "The Boy and the Heron", "Garcon et le heron"]])
citez("Citez un film de la saga Star Wars", "film", "moyen",
      [["La Menace fantôme", "The Phantom Menace", "Episode 1"],
       ["L'Attaque des clones", "Attack of the Clones", "Episode 2"],
       ["La Revanche des Sith", "Revenge of the Sith", "Episode 3"],
       ["Un nouvel espoir", "La Guerre des étoiles", "A New Hope", "Episode 4"],
       ["L'Empire contre-attaque", "The Empire Strikes Back", "Episode 5"],
       ["Le Retour du Jedi", "Return of the Jedi", "Episode 6"],
       ["Le Réveil de la Force", "The Force Awakens", "Episode 7"],
       ["Les Derniers Jedi", "The Last Jedi", "Episode 8"],
       ["L'Ascension de Skywalker", "The Rise of Skywalker", "Episode 9"],
       ["Rogue One"], ["Solo"]])
citez("Citez un film Harry Potter", "film", "moyen",
      [["À l'école des sorciers", "Ecole des sorciers", "Philosopher's Stone", "Sorcerer's Stone"],
       ["La Chambre des secrets", "Chambre des secrets", "Chamber of Secrets"],
       ["Le Prisonnier d'Azkaban", "Azkaban", "Prisoner of Azkaban"],
       ["La Coupe de feu", "Coupe de feu", "Goblet of Fire"],
       ["L'Ordre du Phénix", "Ordre du Phenix", "Order of the Phoenix"],
       ["Le Prince de sang-mêlé", "Prince de sang mele", "Half-Blood Prince"],
       ["Les Reliques de la Mort 1", "Reliques de la mort", "Deathly Hallows"],
       ["Les Reliques de la Mort 2", "Reliques de la mort 2", "Deathly Hallows 2"]])
citez("Citez un membre de l'équipage du Chapeau de paille (One Piece)", "anime", "facile",
      [["Luffy"], ["Zoro"], ["Nami"], ["Usopp"], ["Sanji"], ["Chopper"],
       ["Nico Robin", "Robin"], ["Franky"], ["Brook"], ["Jinbe", "Jimbei"]])
citez("Citez un des 7 nains de Blanche-Neige", "film", "facile",
      [["Prof", "Doc"], ["Grincheux", "Grumpy"], ["Joyeux", "Happy"],
       ["Dormeur", "Sleepy"], ["Timide", "Bashful"], ["Atchoum", "Sneezy"],
       ["Simplet", "Dopey"]])
citez("Citez un des Avengers du premier film (2012)", "film", "facile",
      [["Iron Man", "Tony Stark"], ["Captain America", "Steve Rogers"],
       ["Thor"], ["Hulk", "Bruce Banner"], ["Black Widow", "Veuve noire", "Natasha Romanoff"],
       ["Œil-de-faucon", "Hawkeye", "Oeil de faucon", "Clint Barton"]])
citez("Citez un Pokémon de départ (starter)", "jeuxvideo", "moyen",
      [["Bulbizarre", "Bulbasaur"], ["Salamèche", "Charmander"], ["Carapuce", "Squirtle"],
       ["Germignon", "Chikorita"], ["Héricendre", "Cyndaquil"], ["Kaiminus", "Totodile"],
       ["Arcko", "Treecko"], ["Poussifeu", "Torchic"], ["Gobou", "Mudkip"],
       ["Tortipouss", "Turtwig"], ["Ouisticram", "Chimchar"], ["Tiplouf", "Piplup"],
       ["Vipélierre", "Snivy"], ["Gruikui", "Tepig"], ["Moustillon", "Oshawott"],
       ["Marisson", "Chespin"], ["Feunnec", "Fennekin"], ["Grenousse", "Froakie"],
       ["Brindibou", "Rowlet"], ["Flamiaou", "Litten"], ["Otaquin", "Popplio"],
       ["Ouistempo", "Grookey"], ["Flambino", "Scorbunny"], ["Larméléon", "Sobble"],
       ["Poussacha", "Sprigatito"], ["Chochodile", "Fuecoco"], ["Coiffeton", "Quaxly"],
       ["Pikachu"], ["Évoli", "Eevee", "Evoli"]])
citez("Citez une console de salon Nintendo", "jeuxvideo", "moyen",
      [["NES", "Nintendo Entertainment System"], ["Super Nintendo", "SNES", "Super NES"],
       ["Nintendo 64", "N64"], ["GameCube", "Game Cube"], ["Wii"], ["Wii U"],
       ["Nintendo Switch", "Switch"], ["Switch 2", "Nintendo Switch 2"]])
citez("Citez une console PlayStation (salon ou portable)", "jeuxvideo", "facile",
      [["PlayStation", "PS1", "PlayStation 1"], ["PlayStation 2", "PS2"],
       ["PlayStation 3", "PS3"], ["PlayStation 4", "PS4"], ["PlayStation 5", "PS5"],
       ["PSP", "PlayStation Portable"], ["PS Vita", "PlayStation Vita", "Vita"]])
citez("Citez une pièce du jeu d'échecs", "jeuxsociete", "facile",
      [["Roi", "King"], ["Dame", "Reine", "Queen"], ["Tour", "Rook"],
       ["Fou", "Bishop"], ["Cavalier", "Knight"], ["Pion", "Pawn"]])

# ---------------------------------------------------------------------------
# CULTURE G / SCIENCES / HISTOIRE
# ---------------------------------------------------------------------------
citez("Citez une planète du système solaire", "espace", "facile",
      [["Mercure", "Mercury"], ["Vénus", "Venus"], ["Terre", "Earth"], ["Mars"],
       ["Jupiter"], ["Saturne", "Saturn"], ["Uranus"], ["Neptune"]])
citez("Citez un signe du zodiaque", "culture_g", "facile",
      [["Bélier", "Belier", "Aries"], ["Taureau", "Taurus"], ["Gémeaux", "Gemeaux", "Gemini"],
       ["Cancer"], ["Lion", "Leo"], ["Vierge", "Virgo"], ["Balance", "Libra"],
       ["Scorpion", "Scorpio"], ["Sagittaire", "Sagittarius"], ["Capricorne", "Capricorn"],
       ["Verseau", "Aquarius"], ["Poissons", "Poisson", "Pisces"]])
citez("Citez un animal du zodiaque chinois", "culture_g", "moyen",
      [["Rat"], ["Bœuf", "Boeuf", "Buffle", "Ox"], ["Tigre", "Tiger"],
       ["Lapin", "Lièvre", "Chat", "Rabbit"], ["Dragon"], ["Serpent", "Snake"],
       ["Cheval", "Horse"], ["Chèvre", "Mouton", "Goat", "Chevre"], ["Singe", "Monkey"],
       ["Coq", "Rooster"], ["Chien", "Dog"], ["Cochon", "Porc", "Sanglier", "Pig"]])
citez("Citez une couleur de l'arc-en-ciel", "culture_g", "facile",
      [["Rouge", "Red"], ["Orange"], ["Jaune", "Yellow"], ["Vert", "Green"],
       ["Bleu", "Blue"], ["Indigo"], ["Violet"]])
citez("Citez un mois de l'année qui compte 31 jours", "culture_g", "facile",
      [["Janvier", "January"], ["Mars", "March"], ["Mai", "May"], ["Juillet", "July"],
       ["Août", "Aout", "August"], ["Octobre", "October"], ["Décembre", "Decembre", "December"]])
citez("Citez un gaz noble (gaz rare)", "physique", "difficile",
      [["Hélium", "Helium", "He"], ["Néon", "Neon", "Ne"], ["Argon", "Ar"],
       ["Krypton", "Kr"], ["Xénon", "Xenon", "Xe"], ["Radon", "Rn"],
       ["Oganesson", "Og"]])
citez("Citez un élément chimique dont le symbole tient en UNE seule lettre", "physique",
      "difficile",
      [["Hydrogène", "Hydrogene", "Hydrogen", "H"], ["Bore", "Boron", "B"],
       ["Carbone", "Carbon", "C"], ["Azote", "Nitrogen", "N"], ["Oxygène", "Oxygene", "Oxygen", "O"],
       ["Fluor", "Fluorine", "F"], ["Phosphore", "Phosphorus", "P"], ["Soufre", "Sulfur", "S"],
       ["Potassium", "K"], ["Vanadium", "V"], ["Yttrium", "Y"], ["Iode", "Iodine", "I"],
       ["Tungstène", "Tungstene", "Tungsten", "W"], ["Uranium", "U"]])
citez("Citez un océan", "geographie", "facile",
      [["Océan Pacifique", "Pacifique", "Pacific"], ["Océan Atlantique", "Atlantique", "Atlantic"],
       ["Océan Indien", "Indien", "Indian"], ["Océan Arctique", "Arctique", "Arctic"],
       ["Océan Austral", "Austral", "Antarctique", "Southern"]])
citez("Citez une des 7 merveilles du monde antique", "histoire", "difficile",
      [["Pyramide de Khéops", "Pyramide de Gizeh", "Pyramide", "Kheops", "Pyramides"],
       ["Jardins suspendus de Babylone", "Jardins suspendus", "Babylone"],
       ["Statue de Zeus à Olympie", "Statue de Zeus", "Zeus"],
       ["Temple d'Artémis à Éphèse", "Temple d'Artemis", "Artemis"],
       ["Mausolée d'Halicarnasse", "Mausolee", "Halicarnasse"],
       ["Colosse de Rhodes", "Colosse"], ["Phare d'Alexandrie", "Phare"]])
citez("Citez une des 7 nouvelles merveilles du monde (2007)", "monuments", "moyen",
      [["Grande Muraille de Chine", "Grande Muraille", "Muraille de Chine", "Great Wall"],
       ["Pétra", "Petra"], ["Christ Rédempteur", "Christ redempteur", "Christ de Rio"],
       ["Machu Picchu"], ["Chichén Itzá", "Chichen Itza"], ["Colisée", "Colisee", "Colosseum"],
       ["Taj Mahal"]])
citez("Citez une langue officielle de l'ONU", "langues", "moyen",
      [["Anglais", "English"], ["Français", "Francais", "French"], ["Espagnol", "Spanish"],
       ["Russe", "Russian"], ["Chinois", "Mandarin", "Chinese"], ["Arabe", "Arabic"]])
citez("Citez un continent", "geographie", "facile",
      [["Afrique", "Africa"], ["Amérique", "Amerique", "America", "Amérique du Nord", "Amérique du Sud"],
       ["Antarctique", "Antarctica", "Antarctide"], ["Asie", "Asia"], ["Europe"],
       ["Océanie", "Oceanie", "Australie", "Oceania"]])
citez("Citez un président de l'Algérie (y compris par intérim)", "algerie", "moyen",
      [["Ahmed Ben Bella", "Ben Bella"], ["Houari Boumédiène", "Boumediene"],
       ["Rabah Bitat", "Bitat"], ["Chadli Bendjedid", "Chadli", "Bendjedid"],
       ["Mohamed Boudiaf", "Boudiaf"], ["Ali Kafi", "Kafi"],
       ["Liamine Zéroual", "Zeroual"], ["Abdelaziz Bouteflika", "Bouteflika"],
       ["Abdelkader Bensalah", "Bensalah"], ["Abdelmadjid Tebboune", "Tebboune"]])
citez("Citez un président de la Ve République française", "histoire", "facile",
      [["Charles de Gaulle", "De Gaulle"], ["Georges Pompidou", "Pompidou"],
       ["Valéry Giscard d'Estaing", "Giscard", "VGE"], ["François Mitterrand", "Mitterrand"],
       ["Jacques Chirac", "Chirac"], ["Nicolas Sarkozy", "Sarkozy"],
       ["François Hollande", "Hollande"], ["Emmanuel Macron", "Macron"],
       ["Alain Poher", "Poher"]])
citez("Citez un président des États-Unis", "histoire", "facile",
      [["George Washington", "Washington"], ["John Adams", "John Quincy Adams", "Adams"],
       ["Thomas Jefferson", "Jefferson"], ["James Madison", "Madison"],
       ["James Monroe", "Monroe"], ["Andrew Jackson", "Jackson"],
       ["Martin Van Buren", "Van Buren"],
       ["William Henry Harrison", "Benjamin Harrison", "Harrison"], ["John Tyler", "Tyler"],
       ["James Polk", "Polk"], ["Zachary Taylor", "Taylor"], ["Millard Fillmore", "Fillmore"],
       ["Franklin Pierce", "Pierce"], ["James Buchanan", "Buchanan"],
       ["Abraham Lincoln", "Lincoln"], ["Andrew Johnson", "Lyndon Johnson", "Johnson", "LBJ"],
       ["Ulysses Grant", "Grant"], ["Rutherford Hayes", "Hayes"],
       ["James Garfield", "Garfield"], ["Chester Arthur", "Arthur"],
       ["Grover Cleveland", "Cleveland"], ["William McKinley", "McKinley"],
       ["Theodore Roosevelt", "Franklin Roosevelt", "Roosevelt", "FDR"],
       ["William Taft", "Taft"], ["Woodrow Wilson", "Wilson"],
       ["Warren Harding", "Harding"], ["Calvin Coolidge", "Coolidge"],
       ["Herbert Hoover", "Hoover"], ["Harry Truman", "Truman"],
       ["Dwight Eisenhower", "Eisenhower", "Ike"], ["John F. Kennedy", "Kennedy", "JFK"],
       ["Richard Nixon", "Nixon"], ["Gerald Ford", "Ford"], ["Jimmy Carter", "Carter"],
       ["Ronald Reagan", "Reagan"], ["George Bush", "George W. Bush", "Bush"],
       ["Bill Clinton", "Clinton"], ["Barack Obama", "Obama"],
       ["Donald Trump", "Trump"], ["Joe Biden", "Biden"]])

N_CITEZ = len(OUT)

# ---------------------------------------------------------------------------
# DUELS "Lequel est le plus…" — generes depuis des tables, avec un ecart net
# pour ne jamais tomber sur un cas litigieux.
# ---------------------------------------------------------------------------


def dans_phrase(nom):
    """'Le chat' -> 'le chat', "L'orque" -> "l'orque" (milieu de phrase)."""
    for art in ("Le ", "La ", "Les ", "L'"):
        if nom.startswith(art):
            return art.lower() + nom[len(art):]
    return nom


def generer_duels(table, gabarit, categorie, ratio_min, n, plus_grand=True,
                  ecart_min=None, cle=lambda v: v):
    """table : {nom_ou_tuple_alias: valeur}. Tire n paires au hasard dont
    l'ecart est franc (ratio ou ecart absolu)."""
    items = list(table.items())
    paires = list(itertools.combinations(items, 2))
    random.shuffle(paires)
    faites = 0
    for (a, va), (b, vb) in paires:
        if faites >= n:
            break
        va, vb = cle(va), cle(vb)
        if ecart_min is not None:
            if abs(va - vb) < ecart_min:
                continue
            r = abs(va - vb) / ecart_min
        else:
            lo, hi = sorted([abs(va), abs(vb)])
            if lo == 0 or hi / lo < ratio_min:
                continue
            r = hi / lo / ratio_min
        gagnant, perdant = (a, b) if ((va > vb) == plus_grand) else (b, a)
        na = a if isinstance(a, str) else a[0]
        nb = b if isinstance(b, str) else b[0]
        x, y = [dans_phrase(v) for v in random.sample([na, nb], 2)]
        dif = "facile" if r >= 3 else ("moyen" if r >= 1.6 else "difficile")
        g = [gagnant] if isinstance(gagnant, str) else list(gagnant)
        p = [perdant] if isinstance(perdant, str) else list(perdant)
        duel(gabarit.format(x, y), categorie, dif, g, p)
        faites += 1


def pays(code):
    return tuple(gp(code))


# Population (millions, ordres de grandeur 2024-2025)
POP = {pays("in"): 1440, pays("us"): 340, pays("id"): 280, pays("pk"): 240,
       pays("ng"): 225, pays("br"): 212, pays("bd"): 172, pays("ru"): 144,
       pays("mx"): 130, pays("jp"): 124, pays("et"): 128, pays("ph"): 115,
       pays("eg"): 114, pays("cd"): 105, pays("vn"): 100, pays("ir"): 90,
       pays("tr"): 86, pays("de"): 84, pays("th"): 70, pays("gb"): 68,
       pays("fr"): 68, pays("za"): 63, pays("it"): 59, pays("kr"): 52,
       pays("es"): 48, pays("ar"): 46, pays("dz"): 46, pays("ca"): 41,
       pays("ma"): 37, pays("sa"): 33, pays("pe"): 34, pays("au"): 27,
       pays("sn"): 18, pays("nl"): 18, pays("cl"): 20, pays("tn"): 12,
       pays("be"): 11.8, pays("se"): 10.5, pays("pt"): 10.4, pays("ch"): 9,
       pays("dk"): 6, pays("no"): 5.5, pays("ie"): 5.3, pays("nz"): 5.2,
       pays("qa"): 3, pays("mr"): 5, pays("ly"): 7, pays("is"): 0.39,
       pays("lu"): 0.67, pays("mt"): 0.55, pays("mc"): 0.04, pays("cn"): 1410}
generer_duels(POP, "Lequel a le plus d'habitants : {} ou {} ?", "geographie", 1.8, 30)

# Superficie (milliers de km²)
SUP = {pays("ru"): 17098, pays("ca"): 9985, pays("cn"): 9597, pays("br"): 8516,
       pays("au"): 7692, pays("in"): 3287, pays("ar"): 2780, pays("kz"): 2725,
       pays("dz"): 2382, pays("cd"): 2345, pays("sa"): 2150, pays("mx"): 1964,
       pays("id"): 1905, pays("sd"): 1886, pays("ly"): 1760, pays("ir"): 1648,
       pays("mn"): 1564, pays("pe"): 1285, pays("td"): 1284, pays("ne"): 1267,
       pays("ml"): 1240, pays("za"): 1221, pays("co"): 1142, pays("et"): 1104,
       pays("mr"): 1031, pays("eg"): 1002, pays("ng"): 924, pays("tr"): 784,
       pays("cl"): 756, pays("fr"): 600, pays("mg"): 587, pays("es"): 506,
       pays("se"): 450, pays("jp"): 378, pays("de"): 357, pays("it"): 301,
       pays("gb"): 243, pays("tn"): 163, pays("gr"): 132, pays("pt"): 92,
       pays("is"): 103, pays("ie"): 70, pays("ch"): 41, pays("nl"): 42,
       pays("be"): 30.5, pays("qa"): 11.6, pays("lb"): 10.4, pays("lu"): 2.6,
       pays("mt"): 0.3, pays("mc"): 0.002}
generer_duels(SUP, "Lequel est le plus grand (en superficie) : {} ou {} ?", "geographie",
              1.6, 30)

# Annee de sortie de films tres connus
FILMS = {("Le Parrain", "The Godfather"): 1972, ("Star Wars (1977)", "La Guerre des étoiles", "Star Wars"): 1977,
         ("E.T.", "ET", "E.T. l'extra-terrestre"): 1982,
         ("Retour vers le futur", "Back to the Future"): 1985,
         ("Jurassic Park",): 1993, ("Le Roi lion", "The Lion King", "Roi lion"): 1994,
         ("Pulp Fiction",): 1994, ("Forrest Gump",): 1994, ("Toy Story",): 1995,
         ("Titanic",): 1997, ("Matrix", "The Matrix"): 1999, ("Gladiator",): 2000,
         ("Shrek",): 2001, ("Le Monde de Nemo", "Finding Nemo", "Nemo"): 2003,
         ("The Dark Knight",): 2008, ("Avatar",): 2009, ("Inception",): 2010,
         ("Intouchables",): 2011, ("La Reine des neiges", "Frozen", "Reine des neiges"): 2013,
         ("Interstellar",): 2014, ("Avengers: Endgame", "Endgame"): 2019,
         ("Parasite",): 2019, ("Joker",): 2019, ("Oppenheimer",): 2023, ("Barbie",): 2023,
         ("Les Dents de la mer", "Jaws", "Dents de la mer"): 1975, ("Alien",): 1979,
         ("Terminator",): 1984, ("Psychose", "Psycho"): 1960,
         ("Blanche-Neige et les Sept Nains", "Blanche-Neige", "Snow White"): 1937,
         ("Le Magicien d'Oz", "The Wizard of Oz", "Magicien d'Oz"): 1939,
         ("Casablanca",): 1942, ("Rocky",): 1976,
         ("Les Aventuriers de l'arche perdue", "Indiana Jones", "Raiders of the Lost Ark"): 1981,
         ("Scarface",): 1983, ("Fight Club",): 1999,
         ("Le Voyage de Chihiro", "Chihiro", "Spirited Away"): 2001,
         ("Iron Man",): 2008, ("Black Panther",): 2018, ("Top Gun",): 1986,
         ("Mad Max: Fury Road", "Fury Road"): 2015, ("La Haine",): 1995,
         ("Le Fabuleux Destin d'Amélie Poulain", "Amélie Poulain", "Amelie"): 2001,
         ("Taxi",): 1998, ("Astérix et Obélix : Mission Cléopâtre", "Mission Cleopatre"): 2002,
         ("Bienvenue chez les Ch'tis", "Les Ch'tis", "Chtis"): 2008}
generer_duels(FILMS, "Lequel est sorti en premier : {} ou {} ?", "film", None, 40,
              plus_grand=False, ecart_min=6)

# Monuments : annee de construction (approx.)
MON_AGE = {("Les pyramides de Gizeh", "Pyramides", "Pyramides de Gizeh", "Pyramide"): -2560,
           ("Le Parthénon", "Parthenon", "Parthénon"): -438, ("Le Colisée", "Colisee", "Colisée"): 80,
           ("Notre-Dame de Paris", "Notre-Dame", "Notre Dame"): 1163, ("La tour de Pise", "Tour de Pise", "Pise"): 1173,
           ("Le Taj Mahal", "Taj Mahal"): 1643, ("Le château de Versailles", "Versailles"): 1682,
           ("La tour Eiffel", "Tour Eiffel"): 1889, ("La statue de la Liberté", "Statue de la Liberte"): 1886,
           ("Big Ben",): 1859, ("L'Empire State Building", "Empire State Building", "Empire State"): 1931,
           ("Le Golden Gate Bridge", "Golden Gate"): 1937, ("L'Opéra de Sydney", "Opera de Sydney"): 1973,
           ("Burj Khalifa",): 2010, ("Le Machu Picchu", "Machu Picchu"): 1450,
           ("Angkor Vat", "Angkor", "Angkor Wat"): 1150, ("Maqam Echahid",): 1982,
           ("Notre-Dame d'Afrique",): 1872, ("La Grande Mosquée d'Alger", "Djamaa el Djazair", "Grande mosquee d'Alger"): 2019}
generer_duels(MON_AGE, "Lequel est le plus ancien : {} ou {} ?", "monuments", None, 25,
              plus_grand=False, ecart_min=150)

# Monuments : hauteur (m)
MON_H = {("Burj Khalifa",): 828, ("La tour Eiffel", "Tour Eiffel"): 330,
         ("L'Empire State Building", "Empire State Building", "Empire State"): 443,
         ("La statue de la Liberté", "Statue de la Liberte"): 93,
         ("Le Christ Rédempteur", "Christ Redempteur"): 38,
         ("La pyramide de Khéops", "Pyramide de Kheops", "Kheops"): 139,
         ("La tour de Pise", "Tour de Pise"): 56, ("Le Taj Mahal", "Taj Mahal"): 73,
         ("L'Arc de triomphe", "Arc de triomphe"): 50, ("La Shanghai Tower", "Shanghai Tower"): 632,
         ("Les tours Petronas", "Petronas"): 452, ("Le Colisée", "Colisee", "Colisée"): 48,
         ("Le minaret de Djamaa el Djazaïr", "Djamaa el Djazair", "Grande mosquee d'Alger"): 265}
generer_duels(MON_H, "Lequel est le plus haut : {} ou {} ?", "monuments", 1.4, 22)

# Espace
PLA = {("Mercure", "Mercury"): 4879, ("Vénus", "Venus"): 12104, ("La Terre", "Terre", "Earth"): 12742,
       ("Mars",): 6779, ("Jupiter",): 139820, ("Saturne", "Saturn"): 116460,
       ("Uranus",): 50724, ("Neptune",): 49244, ("La Lune", "Lune", "Moon"): 3474,
       ("Le Soleil", "Soleil", "Sun"): 1392700}
generer_duels(PLA, "Lequel est le plus grand : {} ou {} ?", "espace", 1.3, 20)
ORDRE = {("Mercure", "Mercury"): 1, ("Vénus", "Venus"): 2, ("La Terre", "Terre", "Earth"): 3,
         ("Mars",): 4, ("Jupiter",): 5, ("Saturne", "Saturn"): 6, ("Uranus",): 7,
         ("Neptune",): 8}
generer_duels(ORDRE, "Laquelle est la plus proche du Soleil : {} ou {} ?", "espace", None,
              14, plus_grand=False, ecart_min=1)

# Montagnes (m)
MONT = {("L'Everest", "Everest"): 8849, ("Le K2", "K2"): 8611,
        ("Le Kilimandjaro", "Kilimandjaro"): 5895, ("Le mont Blanc", "Mont Blanc"): 4806,
        ("L'Aconcagua", "Aconcagua"): 6961, ("Le Denali", "Denali", "McKinley"): 6190,
        ("L'Elbrouz", "Elbrouz", "Elbrus"): 5642, ("Le mont Fuji", "Mont Fuji", "Fuji"): 3776,
        ("Le Cervin", "Cervin", "Matterhorn"): 4478, ("Le Tahat", "Tahat"): 2908,
        ("Le Toubkal", "Toubkal"): 4167, ("Le Vésuve", "Vesuve"): 1281,
        ("Le mont Kenya", "Mont Kenya"): 5199, ("Lalla Khedidja", "Lalla Khedidja (Djurdjura)"): 2308}
generer_duels(MONT, "Lequel est le plus haut : {} ou {} ?", "nature", None, 22,
              ecart_min=350)

# Fleuves (km)
FL = {("Le Nil", "Nil", "Nile"): 6650, ("Le Yangtsé", "Yangtse", "Yangtze"): 6300,
      ("Le Danube", "Danube"): 2850, ("Le Rhin", "Rhin", "Rhine"): 1230,
      ("La Seine", "Seine"): 777, ("La Loire", "Loire"): 1006, ("La Tamise", "Tamise", "Thames"): 346,
      ("La Volga", "Volga"): 3530, ("Le Congo", "Congo"): 4700, ("Le Niger", "Niger"): 4180,
      ("Le Gange", "Gange", "Ganges"): 2525, ("Le Mékong", "Mekong"): 4350,
      ("Le Rhône", "Rhone"): 812, ("Le Chélif", "Chelif", "Cheliff"): 733}
generer_duels(FL, "Lequel est le plus long : {} ou {} ?", "geographie", 1.3, 22)

# Animaux : poids (kg) et vitesse (km/h)
POIDS = {("L'éléphant d'Afrique", "Elephant"): 6000, ("L'hippopotame", "Hippopotame", "Hippo"): 1500,
         ("La girafe", "Girafe"): 1200, ("L'ours polaire", "Ours polaire"): 450,
         ("Le lion", "Lion"): 190, ("Le gorille", "Gorille"): 160, ("Le cheval", "Cheval"): 500,
         ("Le zèbre", "Zebre"): 350, ("L'autruche", "Autruche"): 120, ("Le loup", "Loup"): 40,
         ("Le chat", "Chat"): 4.5, ("Le lapin", "Lapin"): 2,
         ("La baleine bleue", "Baleine bleue", "Baleine"): 150000,
         ("Le requin blanc", "Requin blanc", "Requin"): 1100, ("L'orque", "Orque"): 5000,
         ("Le dauphin", "Dauphin"): 200, ("Le crocodile du Nil", "Crocodile"): 500,
         ("Le panda géant", "Panda"): 110, ("Le manchot empereur", "Manchot"): 30}
generer_duels(POIDS, "Lequel est le plus lourd : {} ou {} ?", "animaux", 2.2, 30)
VIT = {("Le guépard", "Guepard"): 110, ("Le lion", "Lion"): 80, ("L'autruche", "Autruche"): 70,
       ("L'éléphant", "Elephant"): 40, ("L'hippopotame", "Hippopotame"): 30,
       ("La tortue", "Tortue"): 0.3, ("L'escargot", "Escargot"): 0.05,
       ("Le faucon pèlerin (en piqué)", "Faucon pelerin", "Faucon"): 390,
       ("Usain Bolt", "Bolt"): 44, ("Le paresseux", "Paresseux"): 0.25,
       ("Le chat domestique", "Chat"): 48}
generer_duels(VIT, "Lequel est le plus rapide : {} ou {} ?", "animaux", 1.8, 22)

# Football : palmares (ecarts francs, valeurs a fin 2026)
BO = {("Lionel Messi", "Messi"): 8, ("Cristiano Ronaldo", "Ronaldo", "CR7"): 5,
      ("Michel Platini", "Platini"): 3, ("Johan Cruyff", "Cruyff"): 3,
      ("Zinédine Zidane", "Zidane"): 1, ("Karim Benzema", "Benzema"): 1,
      ("Luka Modrić", "Modric"): 1, ("Kaká", "Kaka"): 1, ("Ronaldinho",): 1}
generer_duels(BO, "Lequel a gagné le plus de Ballons d'Or : {} ou {} ?", "football", None,
              12, ecart_min=2)
CDM = {pays("br"): 5, pays("de"): 4, pays("it"): 4, pays("ar"): 3, pays("fr"): 2,
       pays("uy"): 2, pays("es"): 2, ("Angleterre", "England"): 1}
generer_duels(CDM, "Lequel a gagné le plus de Coupes du monde : {} ou {} ?", "football",
              None, 12, ecart_min=2)

json.dump(OUT, open("lot_speciales.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"{N_CITEZ} 'Citez-en un' + {len(OUT) - N_CITEZ} duels = {len(OUT)} questions")
