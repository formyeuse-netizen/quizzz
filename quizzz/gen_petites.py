# -*- coding: utf-8 -*-
"""Lot texte "petites categories" (novembre 2026) : corps, logos, instruments,
jeux de societe, langues, aliments, voitures, races, tableaux.
    py gen_petites.py   puis   py charger.py lot_petites.json
"""
import json, random

random.seed(2611)
OUT = []


def q(cat, dif, question, reponse, *alias):
    OUT.append({"categorie": cat, "difficulte": dif, "question": question,
                "reponse": reponse, "alias": list(alias)})


def citez(cat, dif, question, groupes):
    gs = [[g] if isinstance(g, str) else list(g) for g in groupes]
    ex = ", ".join(g[0] for g in gs[:6]) + ("…" if len(gs) > 6 else "")
    OUT.append({"type": "citez", "question": question, "categorie": cat,
                "difficulte": dif, "reponse": f"{ex} ({len(gs)} réponses possibles)",
                "alias": [], "extra": {"groupes": gs}})


def duel(cat, dif, question, bonne, mauvaise):
    b = [bonne] if isinstance(bonne, str) else list(bonne)
    m = [mauvaise] if isinstance(mauvaise, str) else list(mauvaise)
    opts = [b, m]
    random.shuffle(opts)
    OUT.append({"type": "duel", "question": question, "categorie": cat,
                "difficulte": dif, "reponse": b[0], "alias": b[1:],
                "extra": {"options": opts, "bonne": opts.index(b)}})


# =============================================================== CORPS HUMAIN
C = "corps"
q(C, "moyen", "Combien de dents de lait a un enfant ?", "20")
q(C, "moyen", "Combien de cavités (oreillettes + ventricules) compte le cœur ?", "4", "quatre")
q(C, "facile", "Quels organes filtrent le sang pour fabriquer l'urine ?", "les reins", "rein", "reins")
q(C, "facile", "Quel gaz le sang transporte-t-il des poumons vers les organes ?", "l'oxygène", "oxygene", "o2")
q(C, "moyen", "Quel gaz rejette-t-on en expirant, produit par nos cellules ?", "le dioxyde de carbone", "co2", "gaz carbonique", "dioxyde de carbone")
q(C, "difficile", "Quelle protéine des globules rouges transporte l'oxygène ?", "l'hémoglobine", "hemoglobine")
q(C, "moyen", "Quel groupe sanguin est appelé « donneur universel » ?", "O négatif", "o negatif", "o moins", "o")
q(C, "difficile", "Quel groupe sanguin est appelé « receveur universel » ?", "AB positif", "ab plus", "ab")
q(C, "moyen", "Quel muscle en forme de dôme, sous les poumons, permet de respirer ?", "le diaphragme", "diaphragme")
q(C, "difficile", "Quel est le plus gros muscle du corps humain ?", "le grand fessier", "fessier", "fessiers", "grand fessier")
q(C, "moyen", "Combien de litres de sang environ contient le corps d'un adulte ?", "5 litres", "5", "cinq")
q(C, "facile", "Quelle partie colorée de l'œil donne la couleur des yeux ?", "l'iris", "iris")
q(C, "moyen", "Comment s'appelle le trou noir au centre de l'œil qui laisse passer la lumière ?", "la pupille", "pupille")
q(C, "difficile", "Quelle membrane au fond de l'œil capte la lumière ?", "la rétine", "retine")
q(C, "moyen", "Quel organe produit la bile ?", "le foie", "foie")
q(C, "difficile", "Dans quel petit organe la bile est-elle stockée ?", "la vésicule biliaire", "vesicule biliaire", "vesicule")
q(C, "moyen", "Quel est le plus gros organe interne du corps ?", "le foie", "foie")
q(C, "moyen", "Combien de paires de côtes avons-nous ?", "12", "douze")
q(C, "difficile", "Combien de vertèbres compte le cou (vertèbres cervicales) ?", "7", "sept")
q(C, "difficile", "Quelle glande en forme de papillon, dans le cou, règle le métabolisme ?", "la thyroïde", "thyroide")
q(C, "moyen", "Quelle hormone accélère le cœur quand on a peur ?", "l'adrénaline", "adrenaline")
q(C, "difficile", "Quelle hormone, sécrétée la nuit, régule le sommeil ?", "la mélatonine", "melatonine")
q(C, "moyen", "Quelle vitamine la peau fabrique-t-elle grâce au soleil ?", "la vitamine D", "vitamine d")
q(C, "difficile", "Quel pigment donne sa couleur à la peau et aux cheveux ?", "la mélanine", "melanine")
q(C, "moyen", "Quel tendon relie le mollet au talon ?", "le tendon d'Achille", "achille", "tendon d achille")
q(C, "difficile", "Quel poumon est le plus petit, pour laisser de la place au cœur ?", "le gauche", "gauche", "poumon gauche")
q(C, "moyen", "Comment appelle-t-on les vaisseaux qui transportent le sang du cœur vers les organes ?", "les artères", "arteres", "artere")
q(C, "moyen", "Quelle est la plus grosse artère du corps ?", "l'aorte", "aorte")
q(C, "difficile", "Comment s'appellent les plus fins vaisseaux sanguins ?", "les capillaires", "capillaire", "capillaires")
q(C, "moyen", "Quelles cellules du sang défendent le corps contre les infections ?", "les globules blancs", "globule blanc", "leucocytes")
q(C, "difficile", "Quels éléments du sang permettent la coagulation ?", "les plaquettes", "plaquette", "thrombocytes")
q(C, "difficile", "Quelle partie du cerveau gère l'équilibre et la coordination ?", "le cervelet", "cervelet")
q(C, "difficile", "Quelle partie de l'oreille interne a la forme d'un escargot ?", "la cochlée", "cochlee", "limaçon", "limacon")
q(C, "moyen", "Dans quel organe du cou se trouvent les cordes vocales ?", "le larynx", "larynx")
q(C, "moyen", "Quel est le plus long nerf du corps humain ?", "le nerf sciatique", "sciatique")
q(C, "moyen", "Quel os se trouve dans le bras, entre l'épaule et le coude ?", "l'humérus", "humerus")
q(C, "difficile", "Quel os de l'avant-bras se trouve du côté du pouce ?", "le radius", "radius")
q(C, "moyen", "Quel est le gros os à l'avant de la jambe, sous le genou ?", "le tibia", "tibia")
q(C, "facile", "Quelle est la température normale du corps humain (en °C) ?", "37 °C", "37", "37 degres", "37 c")
q(C, "difficile", "Quel tissu, à l'intérieur des os, fabrique les globules rouges ?", "la moelle osseuse", "moelle", "moelle osseuse")
q(C, "moyen", "Combien de chromosomes contient une cellule humaine ?", "46")
q(C, "difficile", "Combien de paires de chromosomes a l'être humain ?", "23")
q(C, "moyen", "Quel organe est surnommé le « deuxième cerveau » ?", "l'intestin", "intestins", "ventre", "intestin")
q(C, "facile", "Quel liquide de la bouche commence la digestion ?", "la salive", "salive")
q(C, "moyen", "Quelle est la matière la plus dure du corps humain ?", "l'émail dentaire", "email", "email des dents", "émail")
q(C, "difficile", "Comment s'appelle l'os de la mâchoire inférieure ?", "la mandibule", "mandibule")
q(C, "difficile", "Quel acide fort se trouve dans l'estomac ?", "l'acide chlorhydrique", "acide chlorhydrique", "hcl")
q(C, "moyen", "Combien de poumons a l'être humain ?", "2", "deux")
citez(C, "facile", "Citez un des cinq sens", ["vue", ["ouïe", "ouie", "audition"], "odorat", "goût", "toucher"])
citez(C, "moyen", "Citez un organe du système digestif",
      ["estomac", ["intestin grêle", "intestin grele"], ["gros intestin", "côlon", "colon"], ["œsophage", "oesophage"],
       "foie", "pancréas", ["bouche", "langue"], "rectum", ["vésicule biliaire", "vesicule"], "anus"])
citez(C, "moyen", "Citez un os du corps humain",
      ["fémur", "tibia", ["péroné", "fibula"], "humérus", "radius", ["cubitus", "ulna"], "crâne", "mandibule",
       ["rotule", "patella"], ["clavicule"], ["omoplate", "scapula"], "sternum", ["côte", "cotes"], ["vertèbre", "vertebres"],
       ["bassin", "os iliaque"], "sacrum", "coccyx", ["étrier", "etrier"], ["marteau"], ["enclume"], ["calcanéum", "calcaneum"],
       ["phalange", "phalanges"]])
duel(C, "moyen", "Quel organe est le plus lourd ?", "le foie", "le cerveau")
duel(C, "moyen", "Qui a le plus d'os ?", "un bébé", "un adulte")
duel(C, "difficile", "Lequel n'est PAS un os ?", "le biceps", "le cubitus")

# ======================================================================= LOGOS
L = "logos"
q(L, "facile", "Quelle marque de vêtements a un crocodile pour logo ?", "Lacoste")
q(L, "facile", "Quelle marque automobile a un cheval cabré noir sur fond jaune ?", "Ferrari")
q(L, "facile", "Quelle marque automobile a un taureau pour emblème ?", "Lamborghini")
q(L, "moyen", "Quelle marque automobile française a un lion pour emblème ?", "Peugeot")
q(L, "facile", "Quelle marque automobile a pour logo quatre anneaux entrelacés ?", "Audi")
q(L, "difficile", "Quelle marque automobile italienne a un trident pour logo ?", "Maserati")
q(L, "moyen", "Quelle marque de sport a un félin bondissant pour logo ?", "Puma")
q(L, "facile", "Quelle chaîne de cafés a une sirène verte pour logo ?", "Starbucks")
q(L, "moyen", "Quelle marque de baskets a un grand « N » sur le côté ?", "New Balance")
q(L, "moyen", "Quelle compagnie pétrolière a un coquillage pour logo ?", "Shell")
q(L, "moyen", "Quelle marque automobile américaine a pour logo un « nœud papillon » doré ?", "Chevrolet", "chevy")
q(L, "difficile", "Quelle marque automobile japonaise a pour logo l'amas d'étoiles des Pléiades ?", "Subaru")
q(L, "moyen", "Quelle marque automobile coréenne a pour logo un « H » penché ?", "Hyundai")
q(L, "facile", "Quelle maison de luxe a pour logo deux « C » entrelacés et dos à dos ?", "Chanel")
q(L, "moyen", "Quelle maison de luxe italienne a pour logo deux « G » entrelacés ?", "Gucci")
q(L, "facile", "Quelle maison de luxe a pour monogramme les lettres « LV » ?", "Louis Vuitton", "vuitton")
q(L, "difficile", "Quelle maison de luxe française a pour logo une calèche tirée par un cheval ?", "Hermès", "hermes")
q(L, "moyen", "Quelle marque de pneus a pour mascotte un bonhomme fait de pneus ?", "Michelin", "bibendum")
q(L, "difficile", "Quelle marque de jeans a une petite étiquette rouge sur la poche arrière ?", "Levi's", "levis", "levi strauss")
q(L, "moyen", "Quelle marque automobile britannique a pour emblème un félin bondissant ?", "Jaguar")
q(L, "difficile", "Quelle marque automobile italienne a dans son logo un serpent qui avale un homme ?", "Alfa Romeo")
q(L, "difficile", "Quelle marque automobile allemande a un cheval cabré au centre d'un blason ?", "Porsche")
q(L, "facile", "Quelle marque a pour slogan « Just Do It » ?", "Nike")
q(L, "moyen", "Quelle marque a pour slogan « Impossible Is Nothing » ?", "Adidas")
q(L, "facile", "Quelle marque de fast-food a pour slogan « I'm lovin' it » ?", "McDonald's", "mcdo", "mcdonalds")
q(L, "difficile", "Quelle marque a utilisé le slogan « Think Different » ?", "Apple")
q(L, "moyen", "Quelle marque de cosmétiques dit « Parce que vous le valez bien » ?", "L'Oréal", "loreal")
q(L, "facile", "Quelle boisson « donne des ailes » et a deux taureaux rouges pour logo ?", "Red Bull", "redbull")
q(L, "facile", "Quelle chaîne de poulet frit a pour visage le colonel Sanders ?", "KFC", "kentucky fried chicken")
q(L, "moyen", "Quelle marque de vêtements a pour logo un joueur de polo à cheval ?", "Ralph Lauren", "polo ralph lauren")
q(L, "difficile", "Quelle marque chinoise de téléphones a pour logo une fleur aux pétales rouges ?", "Huawei")
q(L, "moyen", "Quelle marque de bonbons au chocolat a des lettres « m » imprimées dessus ?", "M&M's", "m&m", "mms", "m et m s")
q(L, "moyen", "Quelle marque de soda a un logo rouge écrit en lettres cursives blanches ?", "Coca-Cola", "coca", "coca cola")
q(L, "moyen", "Quelle marque de jouets danoise a un logo rouge avec des lettres blanches ?", "Lego")
q(L, "difficile", "Quel constructeur automobile suédois a pour logo le symbole du fer (cercle et flèche) ?", "Volvo")
citez(L, "facile", "Citez une marque dont le logo est une lettre ou un monogramme",
      ["McDonald's", "Chanel", "Gucci", "Louis Vuitton", "Hyundai", "Honda", "Facebook", ["Netflix"], "Tesla",
       "Volkswagen", ["Motorola"], ["Pinterest"], ["New Balance"], ["Yves Saint Laurent", "ysl"], "Dior", "Fendi"])
duel(L, "facile", "Quelle marque a une pomme pour logo ?", "Apple", "BlackBerry")
duel(L, "moyen", "Quelle marque a trois diamants rouges pour logo ?", "Mitsubishi", "Suzuki")

# ================================================================= INSTRUMENTS
I = "instruments"
q(I, "facile", "Combien de cordes a un violon ?", "4", "quatre")
q(I, "moyen", "Combien de cordes a une guitare basse standard ?", "4", "quatre")
q(I, "moyen", "Combien de cordes a un ukulélé ?", "4", "quatre")
q(I, "moyen", "À quelle famille d'instruments appartient la trompette ?", "les cuivres", "cuivre", "cuivres")
q(I, "difficile", "Le saxophone est en métal, mais à quelle famille d'instruments appartient-il ?", "les bois", "bois")
q(I, "moyen", "Quel est le plus grand et le plus grave des instruments à cordes frottées ?", "la contrebasse", "contrebasse")
q(I, "difficile", "Quel instrument donne le « la » à l'orchestre pour qu'il s'accorde ?", "le hautbois", "hautbois")
q(I, "moyen", "Quel inventeur belge a donné son nom au saxophone ?", "Adolphe Sax", "sax")
q(I, "facile", "De quel instrument jouait Jimi Hendrix ?", "la guitare électrique", "guitare", "guitare electrique")
q(I, "facile", "De quel instrument jouait Louis Armstrong ?", "la trompette", "trompette")
q(I, "moyen", "De quel instrument jouait John Coltrane ?", "le saxophone", "saxophone", "sax")
q(I, "moyen", "Pour quel instrument Chopin a-t-il écrit presque toute son œuvre ?", "le piano", "piano")
q(I, "difficile", "De quel instrument le virtuose Niccolò Paganini jouait-il ?", "le violon", "violon")
q(I, "moyen", "De quel instrument joue Yo-Yo Ma ?", "le violoncelle", "violoncelle")
q(I, "moyen", "De quel instrument jouait Ringo Starr dans les Beatles ?", "la batterie", "batterie")
q(I, "difficile", "De quel instrument jouait Ravi Shankar ?", "le sitar", "sitar")
q(I, "moyen", "Quel instrument à cordes est emblématique du chaâbi algérois ?", "le mandole", "mandole", "mandol")
q(I, "difficile", "Quel luth à trois cordes est l'instrument central de la musique gnawa ?", "le guembri", "guembri", "gumbri", "sintir", "hajhouj")
q(I, "difficile", "Quelle vièle à une corde, classée à l'UNESCO, est jouée par les femmes touarègues ?", "l'imzad", "imzad")
q(I, "difficile", "Quel tambour joué par les femmes touarègues donne aussi son nom à un genre musical ?", "le tindé", "tinde", "tindi")
q(I, "difficile", "Quelles grosses castagnettes en métal rythment la musique gnawa ?", "les qraqeb", "qraqeb", "karkabou", "krakeb", "qarqabou")
q(I, "moyen", "Quel hautbois traditionnel au son puissant accompagne les fêtes au Maghreb ?", "la zorna", "zorna", "ghaita", "rhaita", "zurna", "ghaïta")
q(I, "facile", "Quel instrument à clavier, fait de tuyaux, trouve-t-on dans les églises ?", "l'orgue", "orgue")
q(I, "moyen", "Comment s'appelle la tige de bois et de crin qui sert à jouer du violon ?", "l'archet", "archet")
q(I, "moyen", "Comment s'appelle la fine lamelle de roseau qui vibre dans une clarinette ?", "l'anche", "anche")
q(I, "difficile", "Quel instrument électronique se joue sans le toucher, en bougeant les mains près de deux antennes ?", "le thérémine", "theremine", "theremin")
q(I, "moyen", "Quel instrument a une coulisse qu'on avance et recule pour changer de note ?", "le trombone", "trombone")
q(I, "facile", "Quel petit instrument de métal en forme de triangle se joue avec une baguette ?", "le triangle", "triangle")
citez(I, "facile", "Citez un instrument à cordes",
      ["guitare", "violon", ["violoncelle"], "contrebasse", ["alto"], "harpe", "piano", "banjo", ["ukulélé", "ukulele"],
       "mandoline", "oud", "mandole", "sitar", ["balalaïka", "balalaika"], ["luth"], ["basse", "guitare basse"],
       ["koto"], ["kora"], ["guembri", "gumbri"], ["clavecin"], ["cithare"], ["qanûn", "qanun", "kanoun"]])
citez(I, "facile", "Citez un instrument à vent",
      ["flûte", "clarinette", "saxophone", "trompette", "trombone", "tuba", ["hautbois"], ["basson"], ["cor"],
       ["harmonica"], ["cornemuse"], ["ney", "nay"], ["zorna", "ghaita"], ["didgeridoo"], ["ocarina"],
       ["flûte de pan"], ["cornet"], ["piccolo"], ["mélodica", "melodica"]])
citez(I, "facile", "Citez un instrument de percussion",
      ["batterie", ["tambour"], ["darbouka", "derbouka"], ["djembé", "djembe"], ["bendir"], ["xylophone"],
       ["triangle"], ["cymbale", "cymbales"], ["timbales", "timbale"], ["maracas"], ["castagnettes"], ["gong"],
       ["tabla"], ["bongos", "bongo"], ["congas", "conga"], ["cajón", "cajon"], ["tambourin", "tambourine"],
       ["vibraphone"], ["marimba"], ["qraqeb", "karkabou"], ["glockenspiel"], ["steel drum"]])
duel(I, "moyen", "Lequel de ces cuivres n'a PAS de pistons ?", "le trombone à coulisse", "la trompette")
duel(I, "difficile", "Le piano est un instrument à…", "cordes (frappées)", "vent")

# ============================================================ JEUX DE SOCIETE
J = "jeuxsociete"
q(J, "moyen", "Combien de pièces chaque joueur a-t-il au début d'une partie d'échecs ?", "16")
q(J, "moyen", "Quel coup spécial des échecs fait bouger le roi et une tour en même temps ?", "le roque", "roque")
q(J, "facile", "Quelle expression annonce la fin d'une partie d'échecs, le roi ne pouvant plus s'échapper ?", "échec et mat", "echec et mat", "mat")
q(J, "difficile", "Comment s'appelle la prise d'un pion qui vient d'avancer de deux cases, par un pion adverse à côté ?", "la prise en passant", "en passant", "prise en passant")
q(J, "moyen", "En quelle pièce transforme-t-on le plus souvent un pion arrivé au bout de l'échiquier ?", "la dame", "dame", "reine")
q(J, "moyen", "Quel joueur norvégien a été champion du monde d'échecs de 2013 à 2023 ?", "Magnus Carlsen", "carlsen")
q(J, "moyen", "Quel ordinateur d'IBM a battu le champion du monde d'échecs en 1997 ?", "Deep Blue")
q(J, "moyen", "Quel champion d'échecs russe a été battu par Deep Blue en 1997 ?", "Garry Kasparov", "kasparov")
q(J, "facile", "Quelle série Netflix suit Beth Harmon, une prodige des échecs ?", "Le Jeu de la dame", "jeu de la dame", "the queen's gambit", "queens gambit")
q(J, "moyen", "Aux échecs, quelle couleur joue toujours le premier coup ?", "les blancs", "blanc", "blancs")
q(J, "moyen", "Combien de pions chaque joueur a-t-il au jeu de dames international ?", "20", "vingt")
q(J, "difficile", "Sur un damier international, combien de cases y a-t-il par côté ?", "10", "dix", "10x10")
q(J, "moyen", "Quelle est la case la plus chère du Monopoly français ?", "rue de la Paix", "la paix")
q(J, "difficile", "Quelle est la première rue qu'on peut acheter après la case Départ au Monopoly français ?", "boulevard de Belleville", "belleville")
q(J, "facile", "Combien de gares y a-t-il sur un plateau de Monopoly ?", "4", "quatre")
q(J, "moyen", "Combien d'armes y a-t-il dans le Cluedo classique ?", "6", "six")
q(J, "moyen", "Combien de lettres a-t-on sur son chevalet au Scrabble ?", "7", "sept")
q(J, "difficile", "Combien de points de bonus rapporte un « scrabble » (poser ses 7 lettres d'un coup) ?", "50", "50 points")
q(J, "moyen", "Combien de cartes distribue-t-on à chaque joueur au début d'une partie de Uno ?", "7", "sept")
q(J, "facile", "Quelle carte Uno fait piocher 4 cartes au joueur suivant ?", "le +4", "plus 4", "4", "super joker", "joker plus 4")
q(J, "moyen", "Sur un dé classique, combien fait la somme de deux faces opposées ?", "7", "sept")
q(J, "difficile", "Combien de points y a-t-il au total sur un dé classique à 6 faces ?", "21")
q(J, "difficile", "Combien de pièces compte un jeu de dominos classique (double-six) ?", "28")
q(J, "moyen", "Combien de cartes compte un jeu de belote ?", "32")
q(J, "moyen", "Combien de cartes compte le jeu espagnol utilisé pour la ronda ?", "40")
q(J, "difficile", "Sur une grille de combien de lignes par côté se joue une partie de go standard ?", "19", "19x19")
q(J, "moyen", "Quel programme de DeepMind a battu le champion de go Lee Sedol en 2016 ?", "AlphaGo", "alpha go")
q(J, "difficile", "Combien de pions (« dames ») chaque joueur a-t-il au backgammon ?", "15")
q(J, "moyen", "Quel architecte hongrois a inventé le Rubik's Cube ?", "Ernő Rubik", "erno rubik", "rubik")
q(J, "moyen", "Aux Colons de Catan, quelle ressource produisent les montagnes ?", "le minerai", "minerai", "pierre")
q(J, "moyen", "Aux Loups-Garous, quel personnage peut découvrir le rôle d'un joueur chaque nuit ?", "la voyante", "voyante")
q(J, "moyen", "Aux Loups-Garous, quel personnage désigne deux amoureux la première nuit ?", "Cupidon")
q(J, "moyen", "Combien de « camemberts » faut-il pour remplir son pion au Trivial Pursuit ?", "6", "six")
q(J, "moyen", "Au Mille Bornes, quelle botte protège contre les crevaisons ?", "l'increvable", "increvable")
q(J, "facile", "Combien de kilomètres faut-il parcourir pour gagner au Mille Bornes ?", "1000", "mille")
q(J, "difficile", "Combien de blocs compte une tour de Jenga ?", "54")
q(J, "moyen", "Combien de colonnes a la grille du Puissance 4 ?", "7", "sept")
q(J, "difficile", "Combien de trous (cases) compte un plateau d'awalé ?", "12", "douze")
q(J, "difficile", "Au tarot, comment s'appelle la carte sans numéro qui permet de ne pas jouer la couleur ?", "l'Excuse", "excuse")
q(J, "difficile", "Au tarot, comment s'appelle le 1 d'atout ?", "le Petit", "petit")
q(J, "moyen", "Quelle est la meilleure main possible au poker ?", "la quinte flush royale", "quinte flush royale", "royal flush")
citez(J, "moyen", "Citez un suspect du Cluedo (version française)",
      [["Moutarde", "colonel moutarde"], ["Rose", "mademoiselle rose"], ["Olive", "docteur olive", "reverend olive"],
       ["Pervenche", "madame pervenche"], ["Violet", "professeur violet"], ["Leblanc", "madame leblanc"]])
citez(J, "facile", "Citez une couleur (enseigne) d'un jeu de cartes classique",
      [["cœur", "coeur"], "carreau", ["trèfle", "trefle"], "pique"])
citez(J, "moyen", "Citez une ressource des Colons de Catan", ["bois", ["argile", "brique"], ["blé", "ble"], ["laine", "mouton"], ["minerai", "pierre"]])
duel(J, "moyen", "Au poker, quelle main gagne ?", "le full", "la couleur")
duel(J, "difficile", "Au Scrabble français, quelle lettre rapporte le plus ?", "le Z", "le M")

# ===================================================================== LANGUES
G = "langues"
for mot, langue, al, dif in [
    ("arigatō", "japonais", [], "facile"), ("gracias", "espagnol", [], "facile"),
    ("grazie", "italien", [], "facile"), ("danke", "allemand", [], "facile"),
    ("choukran", "arabe", [], "facile"), ("spassiba", "russe", [], "moyen"),
    ("teşekkürler", "turc", [], "moyen"), ("xièxie", "chinois", ["mandarin"], "moyen"),
    ("kamsahamnida", "coréen", ["coreen"], "moyen"), ("obrigado", "portugais", [], "facile"),
    ("dank je", "néerlandais", ["neerlandais", "hollandais"], "moyen"),
    ("efcharistó", "grec", [], "difficile"), ("tanemmirt", "kabyle", ["tamazight", "berbere"], "moyen"),
    ("asante", "swahili", [], "difficile"), ("toda", "hébreu", ["hebreu"], "difficile"),
    ("dziękuję", "polonais", [], "difficile"),
]:
    q(G, dif, f"Dans quelle langue dit-on « {mot} » pour remercier ?", langue, *al)
for mot, trad, al, dif in [
    ("merci", "arigatō", ["arigato", "arigatou"], "facile"),
    ("bonjour", "konnichiwa", ["konichiwa"], "moyen"),
]:
    q(G, dif, f"Comment dit-on « {mot} » en japonais ?", trad, *al)
q(G, "facile", "Comment dit-on « merci » en espagnol ?", "gracias")
q(G, "moyen", "Comment dit-on « merci » en kabyle ?", "tanemmirt", "tanmirt")
for pays, langue, al, dif in [
    ("au Brésil", "portugais", [], "facile"), ("au Mexique", "espagnol", [], "facile"),
    ("en Iran", "persan", ["farsi"], "moyen"), ("en Autriche", "allemand", [], "facile"),
    ("en Argentine", "espagnol", [], "facile"), ("en Angola", "portugais", [], "moyen"),
    ("au Suriname", "néerlandais", ["neerlandais", "hollandais"], "difficile"),
    ("au Pakistan (langue nationale)", "ourdou", ["urdu"], "difficile"),
    ("en Israël", "hébreu", ["hebreu"], "moyen"), ("en Éthiopie (langue de travail fédérale)", "amharique", [], "difficile"),
    ("au Mozambique", "portugais", [], "moyen"), ("au Cap-Vert", "portugais", [], "difficile"),
    ("en Guinée équatoriale (langue principale)", "espagnol", [], "difficile"),
]:
    q(G, dif, f"Quelle langue officielle parle-t-on {pays} ?", langue, *al)
q(G, "moyen", "Quelle langue est la langue nationale du Kenya et de la Tanzanie ?", "swahili", "kiswahili")
q(G, "facile", "Quel alphabet utilise la langue russe ?", "cyrillique", "alphabet cyrillique")
q(G, "facile", "Dans quel sens s'écrit l'arabe ?", "de droite à gauche", "droite a gauche")
q(G, "moyen", "Comment s'appelle l'alphabet berbère, avec des lettres comme ⵣ ?", "tifinagh", "tifinar")
q(G, "moyen", "Combien de lettres compte l'alphabet arabe ?", "28")
q(G, "facile", "Combien de lettres compte l'alphabet français ?", "26")
q(G, "difficile", "Combien de lettres compte l'alphabet grec ?", "24")
q(G, "moyen", "Quelle est la dernière lettre de l'alphabet grec ?", "oméga", "omega")
q(G, "moyen", "Les hiragana et les katakana sont des écritures de quelle langue ?", "japonais")
q(G, "moyen", "Le hangul est l'alphabet de quelle langue ?", "coréen", "coreen")
q(G, "moyen", "Quelle langue Zamenhof a-t-il inventée pour qu'elle devienne universelle ?", "espéranto", "esperanto")
q(G, "moyen", "Quelle langue parlent les Klingons dans Star Trek ?", "klingon")
q(G, "difficile", "Quelle langue elfique Tolkien a-t-il inventée pour Le Seigneur des anneaux ?", "quenya", "sindarin", "elfique")
q(G, "moyen", "De quelle langue vient le mot « algèbre » ?", "arabe")
q(G, "difficile", "De quelle langue vient le mot « robot » ?", "tchèque", "tcheque")
q(G, "moyen", "De quelle langue vient le mot « tsunami » ?", "japonais")
q(G, "difficile", "De quelle langue amérindienne vient le mot « chocolat » ?", "nahuatl", "azteque", "aztèque")
q(G, "difficile", "De quelle langue vient le mot « sauna » ?", "finnois", "finlandais")
q(G, "difficile", "De quelle langue vient le mot « safari » ?", "swahili")
q(G, "moyen", "Combien de langues officielles l'ONU compte-t-elle ?", "6", "six")
q(G, "difficile", "Quel sigle désigne la langue des signes française ?", "LSF")
citez(G, "moyen", "Citez une langue officielle de la Suisse", ["allemand", "français", "italien", "romanche"])
citez(G, "moyen", "Citez une langue romane (issue du latin)",
      ["français", "espagnol", "italien", "portugais", "roumain", "catalan", "occitan", ["corse"], ["sarde"],
       ["galicien"], ["romanche"], ["wallon"], ["moldave"]])
citez(G, "difficile", "Citez une langue qui s'écrit avec l'alphabet cyrillique",
      ["russe", "ukrainien", "bulgare", "serbe", ["biélorusse", "bielorusse"], ["macédonien", "macedonien"],
       "kazakh", "mongol", ["kirghize"], ["tadjik"]])
duel(G, "moyen", "Quelle langue a le plus de locuteurs natifs ?", "l'espagnol", "l'anglais")
duel(G, "facile", "Quelle langue s'écrit de droite à gauche ?", "l'hébreu", "le grec")

# ==================================================================== ALIMENTS
A = "aliments"
q(A, "facile", "Avec quel fruit fabrique-t-on le cidre ?", "la pomme", "pomme", "pommes")
q(A, "moyen", "Avec quel fruit fabrique-t-on le poiré ?", "la poire", "poire", "poires")
q(A, "difficile", "De quelle fleur extrait-on le safran ?", "le crocus", "crocus")
q(A, "facile", "Comment appelle-t-on une prune séchée ?", "un pruneau", "pruneau")
q(A, "moyen", "Avec quelle plante fabrique-t-on le tofu ?", "le soja", "soja")
q(A, "facile", "Avec quelle céréale fabrique-t-on la semoule du couscous ?", "le blé", "ble", "ble dur", "blé dur")
q(A, "facile", "Quelle céréale éclate pour donner du popcorn ?", "le maïs", "mais")
q(A, "facile", "Quel fruit à coque est mélangé au cacao dans le Nutella ?", "la noisette", "noisette", "noisettes")
q(A, "moyen", "Quel fruit tropical, surnommé « roi des fruits », est célèbre pour son odeur forte ?", "le durian", "durian")
q(A, "facile", "Quelle vitamine trouve-t-on en abondance dans les agrumes ?", "la vitamine C", "vitamine c", "c")
q(A, "moyen", "De quel continent la pomme de terre est-elle originaire ?", "l'Amérique du Sud", "amerique du sud", "amerique", "andes", "perou")
q(A, "facile", "Quel fruit porte ses graines à l'extérieur ?", "la fraise", "fraise")
q(A, "difficile", "Quel chou vert aux pointes en spirale ressemble à une fractale ?", "le romanesco", "romanesco", "chou romanesco")
q(A, "facile", "Quel légume-fruit est la base du ketchup ?", "la tomate", "tomate")
q(A, "moyen", "Quelle épice jaune-orangé colore le curry ?", "le curcuma", "curcuma")
q(A, "difficile", "Dans quel pays le kiwi est-il originaire ?", "la Chine", "chine")
q(A, "facile", "Quelle céréale cultive-t-on dans des rizières ?", "le riz", "riz")
q(A, "facile", "Quelle légumineuse est la base du houmous ?", "le pois chiche", "pois chiche", "pois chiches")
q(A, "moyen", "Quelle graine est la base de la tahina ?", "le sésame", "sesame")
q(A, "facile", "La deglet nour est une variété de quel fruit ?", "la datte", "datte", "dattes")
q(A, "moyen", "Quel fruit à coque est en réalité une légumineuse, comme les lentilles ?", "la cacahuète", "cacahuete", "arachide")
q(A, "moyen", "Quel fruit sec obtient-on en faisant sécher du raisin ?", "le raisin sec", "raisin sec", "raisins secs")
q(A, "facile", "Quel fruit est utilisé pour faire le guacamole ?", "l'avocat", "avocat")
q(A, "moyen", "Quel légume racine rouge colore le bortsch ?", "la betterave", "betterave")
citez(A, "facile", "Citez un agrume",
      ["orange", "citron", "mandarine", ["clémentine", "clementine"], "pamplemousse", ["citron vert", "lime"],
       "bergamote", "kumquat", "pomelo", "yuzu", ["cédrat", "cedrat"]])
citez(A, "facile", "Citez un fruit rouge",
      ["fraise", "framboise", "cerise", "groseille", "cassis", "myrtille", ["mûre", "mure"],
       ["canneberge", "cranberry"], ["airelle"], ["grenade"]])
citez(A, "moyen", "Citez une légumineuse",
      ["lentille", ["pois chiche", "pois chiches"], ["haricot", "haricots"], ["petit pois", "petits pois"],
       ["fève", "feve"], "soja", ["cacahuète", "arachide"], ["lupin"], ["flageolet"], ["pois cassé", "pois casses"]])
duel(A, "moyen", "Botaniquement, la tomate est…", "un fruit", "un légume")
duel(A, "difficile", "Lequel contient le plus de vitamine C ?", "le kiwi", "l'orange")

# ==================================================================== VOITURES
V = "voitures"
for marque, pays, al, dif in [
    ("Toyota", "Japon", [], "facile"), ("Volvo", "Suède", ["suede"], "moyen"),
    ("Škoda", "République tchèque", ["tchequie", "republique tcheque", "tchéquie"], "moyen"),
    ("Seat", "Espagne", [], "moyen"), ("Hyundai", "Corée du Sud", ["coree", "coree du sud"], "facile"),
    ("Dacia", "Roumanie", [], "moyen"), ("Fiat", "Italie", [], "facile"),
    ("Tata", "Inde", [], "moyen"), ("Lada", "Russie", [], "moyen"),
    ("Opel", "Allemagne", [], "moyen"), ("Land Rover", "Royaume-Uni", ["angleterre", "royaume uni", "uk"], "moyen"),
    ("Geely", "Chine", [], "difficile"), ("BYD", "Chine", [], "moyen"), ("Kia", "Corée du Sud", ["coree", "coree du sud"], "moyen"),
    ("Saab", "Suède", ["suede"], "difficile"), ("Proton", "Malaisie", [], "difficile"),
]:
    q(V, dif, f"De quel pays vient la marque automobile {marque} ?", pays, *al)
q(V, "difficile", "Dans quelle ville italienne se trouve le siège de Ferrari ?", "Maranello")
q(V, "moyen", "Quel modèle Renault a été le premier assemblé en Algérie, à Oued Tlélat ?", "Renault Symbol", "symbol")
q(V, "moyen", "Quelle marque assemble ses voitures à l'usine de Tafraoui, près d'Oran, depuis fin 2023 ?", "Fiat")
q(V, "facile", "Quelle célèbre course automobile d'endurance dure 24 heures en France ?", "les 24 Heures du Mans", "le mans", "24 heures du mans")
q(V, "moyen", "Quelle marque fabrique la Model Y ?", "Tesla")
q(V, "difficile", "Que signifie le sigle SUV ?", "Sport Utility Vehicle")
q(V, "moyen", "Quel fabricant de tracteurs italien a créé une marque pour concurrencer Ferrari ?", "Lamborghini", "ferruccio lamborghini")
q(V, "facile", "Quelle marque allemande signifie « voiture du peuple » ?", "Volkswagen", "vw")
q(V, "moyen", "Quelle marque britannique est associée à James Bond depuis Goldfinger ?", "Aston Martin")
q(V, "moyen", "Quelle est la voiture la plus vendue de l'histoire ?", "la Toyota Corolla", "corolla", "toyota corolla")
q(V, "moyen", "Quel pays produit le plus de voitures au monde ?", "la Chine", "chine")
q(V, "moyen", "Qui a fondé la marque Ford ?", "Henry Ford")
q(V, "moyen", "Quelle marque de luxe britannique a pour emblème « l'Esprit d'extase » sur le capot ?", "Rolls-Royce", "rolls royce", "rolls")
q(V, "difficile", "Quelle marque française de voitures de sport a fabriqué la Veyron et la Chiron ?", "Bugatti")
citez(V, "facile", "Citez une marque automobile allemande",
      ["Volkswagen", "BMW", ["Mercedes", "mercedes-benz"], "Audi", "Porsche", "Opel", ["Maybach"], ["Smart"]])
citez(V, "facile", "Citez une marque automobile japonaise",
      ["Toyota", "Honda", "Nissan", "Mazda", "Subaru", "Mitsubishi", "Suzuki", "Lexus", "Infiniti",
       "Daihatsu", "Isuzu", "Acura"])
citez(V, "moyen", "Citez une marque automobile italienne",
      ["Fiat", "Ferrari", "Lamborghini", "Maserati", ["Alfa Romeo"], "Lancia", "Pagani", "Abarth"])
citez(V, "facile", "Citez une marque automobile française",
      ["Renault", "Peugeot", ["Citroën", "citroen"], "Bugatti", "Alpine", ["DS"]])
duel(V, "moyen", "Quelle marque appartient au groupe Volkswagen ?", "Porsche", "Ferrari")
duel(V, "difficile", "Quelle marque est la plus ancienne ?", "Peugeot", "Renault")

# ======================================================================= RACES
R = "races"
q(R, "moyen", "De quelle race est Milou, le chien de Tintin ?", "fox-terrier", "fox terrier", "terrier")
q(R, "moyen", "De quelle race est Scooby-Doo ?", "dogue allemand", "dogue", "danois", "grand danois")
q(R, "moyen", "De quelle race est Snoopy ?", "beagle")
q(R, "moyen", "De quelle race est Lassie ?", "colley", "collie")
q(R, "facile", "Quelle race de chien est la plus petite du monde ?", "chihuahua")
q(R, "moyen", "Quelle race de chien est la plus rapide à la course ?", "lévrier", "levrier", "greyhound", "levrier anglais")
q(R, "facile", "Quelle race de chat n'a presque pas de poils ?", "sphynx", "sphinx")
q(R, "moyen", "Quelle race de chat a les oreilles pliées vers l'avant ?", "scottish fold")
q(R, "difficile", "Quel lévrier élancé est élevé par les Touaregs du Sahel ?", "azawakh")
q(R, "moyen", "Quel lévrier du Maghreb est une race algérienne et marocaine ?", "sloughi")
q(R, "facile", "Quelle race de chien de traîneau a souvent les yeux bleus ?", "husky", "husky siberien")
q(R, "facile", "Quel chien sauveteur des Alpes est représenté avec un tonnelet ?", "saint-bernard", "saint bernard")
q(R, "facile", "De quelle race sont les chiots des « 101 » du film Disney ?", "dalmatien")
q(R, "moyen", "Quelle race de chat est la plus grande parmi les chats domestiques ?", "maine coon")
q(R, "moyen", "De quelle race était Hachikō, le chien fidèle de Tokyo ?", "akita", "akita inu")
q(R, "moyen", "Quelle race de chien aimait la reine Elizabeth II ?", "corgi", "welsh corgi")
q(R, "moyen", "Quelle race de chien a une langue bleu-noir ?", "chow-chow", "chow chow")
q(R, "difficile", "Quelle race de chat thaïlandais a un corps clair et le bout des pattes, oreilles et queue foncé ?", "siamois")
q(R, "difficile", "Quel grand berger d'Anatolie est utilisé pour protéger les troupeaux contre les loups ?", "kangal", "berger d anatolie")
citez(R, "moyen", "Citez une race de chien de berger",
      [["berger allemand"], ["malinois", "berger belge"], ["border collie"], ["berger australien"], ["colley", "collie"],
       ["bouvier bernois"], ["beauceron"], ["briard", "berger de brie"], ["corgi"], ["kangal"], ["berger blanc suisse"]])
citez(R, "moyen", "Citez une race de chat",
      ["siamois", "persan", ["maine coon"], "sphynx", "bengal", "chartreux", ["british shorthair"], "ragdoll",
       ["sacré de birmanie", "birman"], ["bleu russe"], ["scottish fold"], "abyssin", "angora", "savannah",
       ["norvégien", "norvegien"], ["exotic shorthair"], ["turc de van"]])
duel(R, "moyen", "Quelle race de chien est la plus grande ?", "le dogue allemand", "le berger allemand")

# ==================================================================== TABLEAUX
T = "tableaux"
for oeuvre, peintre, al, dif in [
    ("La Nuit étoilée", "Vincent van Gogh", ["van gogh"], "facile"),
    ("Le Cri", "Edvard Munch", ["munch"], "moyen"),
    ("Guernica", "Pablo Picasso", ["picasso"], "facile"),
    ("La Persistance de la mémoire (les montres molles)", "Salvador Dalí", ["dali"], "moyen"),
    ("La Jeune Fille à la perle", "Johannes Vermeer", ["vermeer"], "moyen"),
    ("La Ronde de nuit", "Rembrandt", [], "moyen"),
    ("La Création d'Adam", "Michel-Ange", ["michel ange", "michelangelo"], "moyen"),
    ("Le Baiser (1908, feuilles d'or)", "Gustav Klimt", ["klimt"], "moyen"),
    ("La Liberté guidant le peuple", "Eugène Delacroix", ["delacroix"], "moyen"),
    ("Les Nymphéas", "Claude Monet", ["monet"], "moyen"),
    ("La Naissance de Vénus", "Sandro Botticelli", ["botticelli"], "moyen"),
    ("Les Ménines", "Diego Velázquez", ["velazquez", "velasquez"], "difficile"),
    ("Le Radeau de la Méduse", "Théodore Géricault", ["gericault"], "difficile"),
    ("American Gothic", "Grant Wood", ["wood"], "difficile"),
    ("Les Demoiselles d'Avignon", "Pablo Picasso", ["picasso"], "moyen"),
    ("Femmes d'Alger dans leur appartement (1834)", "Eugène Delacroix", ["delacroix"], "difficile"),
    ("La Grande Vague de Kanagawa", "Hokusai", ["katsushika hokusai"], "difficile"),
    ("Le Fils de l'homme (l'homme à la pomme verte)", "René Magritte", ["magritte"], "moyen"),
]:
    q(T, dif, f"Qui a peint « {oeuvre} » ?", peintre, *al)
q(T, "facile", "Quelle peintre mexicaine est célèbre pour ses autoportraits aux sourcils joints ?", "Frida Kahlo", "frida", "kahlo")
q(T, "moyen", "Quel artiste du pop art a peint des boîtes de soupe Campbell ?", "Andy Warhol", "warhol")
q(T, "moyen", "Quel artiste de rue britannique anonyme a créé « La Petite Fille au ballon » ?", "Banksy")
q(T, "facile", "Dans quel musée parisien est exposée La Joconde ?", "le Louvre", "louvre", "musee du louvre")
q(T, "moyen", "Quel peintre algérien est célèbre pour ses miniatures et enluminures ?", "Mohammed Racim", "racim")
q(T, "difficile", "Quel peintre orientaliste français, converti à l'islam, a vécu à Bou Saâda ?", "Étienne Dinet", "dinet", "nasreddine dinet")
q(T, "difficile", "Quelle peintre algérienne autodidacte, née Fatma Haddad, a exposé à Paris dès 1947 ?", "Baya", "baya mahieddine")
q(T, "moyen", "Quel mouvement artistique tire son nom du tableau « Impression, soleil levant » ?", "l'impressionnisme", "impressionnisme")
q(T, "moyen", "Quel mouvement de Picasso et Braque décompose les formes en facettes ?", "le cubisme", "cubisme")
q(T, "moyen", "Quel mouvement de Dalí et Magritte s'inspire des rêves ?", "le surréalisme", "surrealisme")
q(T, "moyen", "Quel peintre belge a écrit « Ceci n'est pas une pipe » sous un tableau ?", "René Magritte", "magritte")
citez(T, "moyen", "Citez un peintre impressionniste",
      [["Monet", "claude monet"], ["Renoir"], ["Degas"], ["Pissarro"], ["Sisley"], ["Manet"], ["Berthe Morisot", "morisot"],
       ["Caillebotte"], ["Cézanne", "cezanne"], ["Mary Cassatt", "cassatt"]])
duel(T, "facile", "Qui a peint La Cène ?", "Léonard de Vinci", "Raphaël")
duel(T, "moyen", "Qui a peint Les Tournesols ?", "Van Gogh", "Gauguin")

json.dump(OUT, open("lot_petites.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
print(len(OUT), Counter(x["categorie"] for x in OUT))
