# -*- coding: utf-8 -*-
"""Lot texte de novembre 2026 : jeux video, langues, jeux de societe, anime.
    py gen_texte_nov.py   puis   py charger.py lot_texte_nov.json
"""
import json

OUT = []


def q(cat, dif, question, reponse, *alias):
    OUT.append({"categorie": cat, "difficulte": dif, "question": question,
                "reponse": reponse, "alias": list(alias)})


# --------------------------------------------------------------- JEUX VIDEO
J = "jeuxvideo"
q(J, "facile", "Dans quel jeu construit-on avec des blocs en évitant les Creepers ?", "Minecraft")
q(J, "facile", "Dans quel battle royale d'Epic Games saute-t-on d'un bus volant et construit-on des murs ?", "Fortnite")
q(J, "facile", "Dans quel jeu doit-on démasquer l'imposteur à bord d'un vaisseau spatial ?", "Among Us")
q(J, "moyen", "Quel jeu de Riot Games oppose deux équipes de 5 champions sur la Faille de l'invocateur ?", "League of Legends", "LoL")
q(J, "moyen", "Quel FPS tactique de Riot Games oppose des « agents » aux pouvoirs spéciaux ?", "Valorant")
q(J, "moyen", "Quel jeu de tir en équipe de Blizzard met en scène des héros comme Tracer et Mercy ?", "Overwatch")
q(J, "facile", "Dans quel jeu de combat de Capcom Ryu et Ken lancent-ils des « Hadouken » ?", "Street Fighter")
q(J, "facile", "Dans quel jeu une boule jaune mange des pac-gommes en fuyant des fantômes ?", "Pac-Man", "Pacman")
q(J, "moyen", "Quel jeu d'arcade de 1978 fait tirer sur des vagues d'extraterrestres qui descendent ?", "Space Invaders")
q(J, "difficile", "Quel jeu d'Atari de 1972, inspiré du tennis de table, est l'un des premiers jeux vidéo ?", "Pong")
q(J, "moyen", "Dans quel jeu Joel et Ellie traversent-ils une Amérique ravagée par un champignon ?", "The Last of Us", "Last of Us")
q(J, "facile", "Dans quelle série le guerrier spartiate Kratos affronte-t-il les dieux ?", "God of War")
q(J, "moyen", "Dans quelle série d'horreur affronte-t-on les zombies créés par Umbrella Corporation ?", "Resident Evil", "Biohazard")
q(J, "difficile", "Quel jeu de FromSoftware, coécrit avec George R. R. Martin, se déroule dans l'Entre-terre ?", "Elden Ring")
q(J, "moyen", "Dans quelle série de RPG de Square Enix croise-t-on des chocobos et le héros Cloud ?", "Final Fantasy", "FF")
q(J, "moyen", "Dans quelle série Sora voyage-t-il avec Donald et Dingo dans les mondes Disney ?", "Kingdom Hearts")
q(J, "facile", "Dans quel jeu de Nintendo vit-on dans un village d'animaux en remboursant Tom Nook ?", "Animal Crossing")
q(J, "moyen", "Dans quel jeu de Nintendo des calamars humanoïdes s'affrontent-ils à coups d'encre ?", "Splatoon")
q(J, "moyen", "Dans quel jeu de Valve crée-t-on des passages avec un pistolet, sous l'œil de GLaDOS ?", "Portal")
q(J, "moyen", "Dans quelle série incarne-t-on Geralt de Riv, un chasseur de monstres ?", "The Witcher", "Witcher")
q(J, "moyen", "Dans quel jeu de CD Projekt explore-t-on Night City avec Keanu Reeves ?", "Cyberpunk 2077", "Cyberpunk")
q(J, "facile", "Dans quel jeu joue-t-on au football avec des voitures ?", "Rocket League")
q(J, "facile", "Dans quel jeu mobile de Supercell construit-on un village et attaque-t-on avec des barbares ?", "Clash of Clans")
q(J, "facile", "Dans quel jeu mobile aligne-t-on des bonbons de même couleur ?", "Candy Crush", "Candy Crush Saga")
q(J, "facile", "Dans quel jeu lance-t-on des oiseaux avec un lance-pierre sur des cochons ?", "Angry Birds")
q(J, "facile", "Dans quel jeu mobile court-on sur les rails du métro pour fuir un inspecteur et son chien ?", "Subway Surfers")
q(J, "facile", "Quelle plateforme de jeux créés par les joueurs a sa monnaie, les Robux ?", "Roblox")
q(J, "moyen", "Dans quel jeu explore-t-on le monde de Teyvat en invoquant des personnages ?", "Genshin Impact", "Genshin")
q(J, "moyen", "Dans quel jeu reprend-on la ferme de son grand-père dans la vallée de Pélican Bourg ?", "Stardew Valley")
q(J, "difficile", "Dans quel jeu un petit chevalier insecte explore-t-il le royaume souterrain d'Hallownest ?", "Hollow Knight")
q(J, "difficile", "Dans quel jeu un enfant tombé sous terre peut-il épargner tous les monstres, comme Sans ?", "Undertale")
q(J, "moyen", "Dans quel jeu au style dessin animé des années 1930 incarne-t-on une tasse ?", "Cuphead")
q(J, "moyen", "Quel petit dragon violet est le héros d'une série de plateforme sur PlayStation ?", "Spyro")
q(J, "moyen", "Dans quelle série un prince manipule-t-il les Sables du temps ?", "Prince of Persia")
q(J, "facile", "Quelle aventurière archéologue est l'héroïne de Tomb Raider ?", "Lara Croft", "Lara")
q(J, "moyen", "Quelle série de course d'EA est connue pour ses courses-poursuites avec la police ?", "Need for Speed", "NFS")
q(J, "moyen", "Quel jeu de football de Konami, longtemps appelé PES, porte aujourd'hui un autre nom ?", "eFootball", "e Football")
q(J, "moyen", "Comment s'appelle le jeu de football d'EA Sports qui a remplacé FIFA en 2023 ?", "EA Sports FC", "EA FC", "FC 24", "FC 25", "FC 26")
q(J, "moyen", "Dans quel FPS tactique d'Ubisoft des opérateurs attaquent-ils ou défendent-ils un bâtiment ?", "Rainbow Six Siege", "Rainbow Six", "R6")
q(J, "moyen", "Quel battle royale de 2017 récompense le vainqueur d'un « Winner Winner Chicken Dinner » ?", "PUBG", "PlayerUnknown's Battlegrounds")
q(J, "facile", "Dans quel jeu des petits haricots colorés font-ils des courses d'obstacles ?", "Fall Guys")
q(J, "moyen", "Quel FPS de 1993 envoie un marine combattre des démons sur une base martienne ?", "Doom")
q(J, "moyen", "Dans quel jeu en ligne de Blizzard la Horde et l'Alliance s'affrontent-elles en Azeroth ?", "World of Warcraft", "WoW")
q(J, "difficile", "Dans quel jeu de stratégie s'affrontent les Terrans, les Zergs et les Protoss ?", "StarCraft")
q(J, "difficile", "Dans quel jeu guide-t-on des petites créatures aux cheveux verts qui marchent vers le vide ?", "Lemmings")
q(J, "moyen", "Dans quel jeu pose-t-on des bombes dans un labyrinthe pour éliminer ses adversaires ?", "Bomberman")
q(J, "difficile", "Dans quel jeu d'arcade une grenouille doit-elle traverser une route puis une rivière ?", "Frogger")
q(J, "moyen", "Dans quel jeu le samouraï Jin Sakai défend-il son île contre l'invasion mongole ?", "Ghost of Tsushima")
q(J, "difficile", "Dans quel jeu du studio français Quantic Dream incarne-t-on des androïdes ?", "Detroit: Become Human", "Detroit")
q(J, "moyen", "Dans quel jeu un cube saute-t-il au rythme de la musique pour éviter des pics ?", "Geometry Dash")
q(J, "facile", "Dans quel jeu mobile de 2013 un oiseau doit-il passer entre des tuyaux verts ?", "Flappy Bird")
q(J, "facile", "Dans quel jeu défend-on sa maison avec des tournesols et des pois contre des zombies ?", "Plants vs. Zombies", "Plantes contre zombies", "Plants vs Zombies")
q(J, "moyen", "Dans quel jeu joue-t-on de la musique avec une guitare en plastique à 5 boutons de couleur ?", "Guitar Hero")
q(J, "facile", "Quel jeu livré avec la Wii proposait bowling, tennis et boxe avec les Mii ?", "Wii Sports")
q(J, "moyen", "Dans quel jeu un tueur traque-t-il 4 survivants qui réparent des générateurs ?", "Dead by Daylight")
q(J, "facile", "Comment s'appelle le frère de Mario, habillé en vert ?", "Luigi")
q(J, "facile", "Comment s'appelle le petit dinosaure vert que chevauche Mario ?", "Yoshi")
q(J, "facile", "Comment s'appelle la princesse du Royaume Champignon ?", "Peach", "Princesse Peach")
q(J, "facile", "Comment s'appelle la tortue géante, grand méchant des jeux Mario ?", "Bowser")
q(J, "facile", "Comment s'appelle le héros en tunique verte de The Legend of Zelda ?", "Link")
q(J, "moyen", "Comment s'appelle le savant moustachu, ennemi juré de Sonic ?", "Docteur Eggman", "Eggman", "Robotnik", "Dr Eggman", "Dr Robotnik")
q(J, "difficile", "Quel créateur japonais a inventé Mario et Zelda ?", "Shigeru Miyamoto", "Miyamoto")
q(J, "moyen", "Quel studio a créé la série GTA ?", "Rockstar Games", "Rockstar")
q(J, "facile", "Quelle entreprise fabrique la console Xbox ?", "Microsoft")
q(J, "facile", "Quelle entreprise japonaise fabrique les consoles PlayStation ?", "Sony")

# ------------------------------------------------------------------ LANGUES
L = "langues"
LQ = "Quelle est cette langue : « {} » ?"
for salut, rep, dif, al in [
    ("Azul · ⴰⵣⵓⵍ", "tamazight", "facile", ["berbère", "berbere", "kabyle", "amazigh", "chaoui"]),
    ("Wech rak ?", "darja", "facile", ["arabe algérien", "algérien", "algerien", "derja", "arabe", "dziri"]),
    ("Дякую (diakouïou)", "ukrainien", "moyen", ["ukrainian"]),
    ("Здравей (zdravei)", "bulgare", "difficile", ["bulgarian"]),
    ("Dobar dan", "croate", "difficile", ["serbe", "bosnien", "bosniaque", "serbo-croate", "croatian", "serbian"]),
    ("Dobrý deň", "slovaque", "difficile", ["slovak"]),
    ("Dober dan", "slovène", "difficile", ["slovene", "slovenian"]),
    ("Tere", "estonien", "difficile", ["estonian"]),
    ("Labdien", "letton", "difficile", ["latvian"]),
    ("Laba diena", "lituanien", "difficile", ["lithuanian"]),
    ("Mange tak", "danois", "moyen", ["danish"]),
    ("Tusen takk", "norvégien", "moyen", ["norvegien", "norwegian"]),
    ("Góðan daginn", "islandais", "difficile", ["icelandic"]),
    ("Bore da", "gallois", "difficile", ["welsh"]),
    ("Demat", "breton", "difficile", []),
    ("Bon dia", "catalan", "moyen", []),
    ("Bonġu", "maltais", "difficile", ["maltese"]),
    ("Moien", "luxembourgeois", "difficile", ["luxembourgish"]),
    ("درود (dorud)", "persan", "difficile", ["farsi", "iranien", "persian"]),
    ("Silav", "kurde", "difficile", ["kurdish", "kurmandji"]),
    ("Assalomu alaykum", "ouzbek", "difficile", ["uzbek"]),
    ("ਸਤ ਸ੍ਰੀ ਅਕਾਲ (sat srī akāl)", "pendjabi", "difficile", ["punjabi", "panjabi"]),
    ("ආයුබෝවන් (āyubōvan)", "cingalais", "difficile", ["sinhala", "singhalais"]),
    ("བཀྲ་ཤིས་བདེ་ལེགས། (tashi delek)", "tibétain", "difficile", ["tibetain", "tibetan"]),
    ("ສະບາຍດີ (sabaidi)", "lao", "difficile", ["laotien"]),
    ("សួស្តី (suosdei)", "khmer", "difficile", ["cambodgien"]),
    ("မင်္ဂလာပါ (mingalaba)", "birman", "difficile", ["burmese", "myanmar"]),
    ("Сайн байна уу (sain baina uu)", "mongol", "difficile", ["mongolian"]),
    ("Kia ora", "maori", "moyen", ["māori"]),
    ("Talofa", "samoan", "difficile", []),
    ("Ia ora na", "tahitien", "difficile", ["tahitian"]),
    ("Bula", "fidjien", "difficile", ["fijian"]),
    ("Nanga def", "wolof", "moyen", []),
    ("Sannu", "haoussa", "difficile", ["hausa", "haousa"]),
    ("Mbote", "lingala", "moyen", []),
    ("Manao ahoana", "malgache", "moyen", ["malagasy"]),
    ("Goeie môre", "afrikaans", "moyen", []),
    ("Iska warran", "somali", "difficile", []),
    ("Muraho", "kinyarwanda", "difficile", ["rwandais"]),
    ("Allillanchu", "quechua", "difficile", ["kichwa"]),
]:
    q(L, dif, LQ.format(salut), rep, *al)

# --------------------------------------------------------- JEUX DE SOCIETE
S = "jeuxsociete"
q(S, "facile", "Quel jeu de cartes, très joué en Algérie, consiste à ramasser les cartes de même valeur en annonçant « Ronda » ou « Tringa » ?", "Ronda")
q(S, "moyen", "Quel jeu de cartes tunisien tire son nom du jeu italien « scopa » ?", "Chkobba", "Chkoba", "Scopa")
q(S, "facile", "Dans quel jeu de cartes annonce-t-on « belote… rebelote » avec le roi et la dame d'atout ?", "Belote")
q(S, "moyen", "Quel jeu de cartes français se joue avec 78 cartes dont 21 atouts et l'Excuse ?", "Tarot")
q(S, "facile", "Dans quel jeu de cartes de casino faut-il approcher 21 sans le dépasser ?", "Blackjack", "Black Jack", "21", "Vingt-et-un")
q(S, "facile", "Dans quel jeu de cartes et de bluff vise-t-on une quinte flush ou un carré d'as ?", "Poker")
q(S, "facile", "Quel jeu de cartes simple se joue en retournant chacun une carte, la plus forte remportant le pli ?", "Bataille", "La bataille")
q(S, "facile", "Dans quel jeu de cartes réunit-on les membres d'une même famille en les demandant aux autres ?", "Jeu des 7 familles", "7 familles", "Sept familles")
q(S, "facile", "Dans quel jeu de papier faut-il aligner trois croix ou trois ronds dans une grille de 3 × 3 ?", "Morpion", "Tic-tac-toe")
q(S, "facile", "Dans quel jeu devine-t-on un mot lettre par lettre avant que le dessin du bonhomme soit terminé ?", "Pendu", "Le pendu")
q(S, "facile", "Dans quel jeu trouve-t-on un pays, un prénom, un animal… commençant tous par la même lettre ?", "Petit Bac", "Baccalauréat", "Le petit bac")
q(S, "moyen", "Quel jeu de dés de bar porte le nom de sa meilleure combinaison ?", "421", "Quatre cent vingt et un")
q(S, "moyen", "Dans quel jeu lance-t-on 5 dés pour réaliser full, carré, brelan ou suite ?", "Yam's", "Yams", "Yahtzee", "Yatzy")
q(S, "moyen", "Dans quel jeu secoue-t-on 16 dés-lettres pour trouver un maximum de mots en 3 minutes ?", "Boggle")
q(S, "moyen", "Dans quel jeu devine-t-on une combinaison secrète de pions colorés grâce à des indices noirs et blancs ?", "Mastermind")
q(S, "difficile", "Dans quel jeu les pièces ont un grade caché et il faut capturer le drapeau adverse ?", "Stratego")
q(S, "moyen", "Dans quel jeu retourne-t-on les pions noirs et blancs de l'adversaire en les encadrant ?", "Othello", "Reversi")
q(S, "moyen", "Dans quel jeu fait-on glisser des tuiles couloir pour atteindre des trésors ?", "Labyrinthe")
q(S, "moyen", "Dans quel jeu relie-t-on des villes avec des wagons pour réaliser ses billets de destination ?", "Les Aventuriers du Rail", "Aventuriers du rail", "Ticket to Ride")
q(S, "moyen", "Dans quel jeu deux maîtres-espions donnent-ils un mot et un nombre pour faire trouver leurs agents ?", "Codenames", "Nom de code")
q(S, "difficile", "Dans quel jeu de cartes notées de -2 à 12 élimine-t-on les colonnes de 3 cartes identiques ?", "Skyjo")
q(S, "difficile", "Dans quel jeu incarne-t-on des marchands de pierres précieuses qui achètent mines et caravanes ?", "Splendor")
q(S, "difficile", "Dans quel jeu compose-t-on une mosaïque de carreaux de faïence portugais ?", "Azul")
q(S, "difficile", "Dans quel jeu des peuples fantastiques en déclin se disputent-ils un monde trop petit ?", "Small World")
q(S, "moyen", "Dans quel jeu des hippopotames colorés avalent-ils des billes le plus vite possible ?", "Hippos Gloutons", "Hippo glouton", "Hungry Hippos")
q(S, "moyen", "Dans quel jeu fait-on tourner une roue et avance-t-on une voiture remplie de petits pions famille ?", "Destins : le jeu de la vie", "Destins", "Le jeu de la vie", "Game of Life")

# -------------------------------------------------------------------- ANIME
A = "anime"
q(A, "facile", "Quel pirate au chapeau de paille veut devenir le Roi des pirates ?", "Monkey D. Luffy", "Luffy")
q(A, "facile", "Quel épéiste aux trois sabres est le second de Luffy ?", "Roronoa Zoro", "Zoro")
q(A, "moyen", "Dans Death Note, quel est le vrai nom du détective excentrique qui se fait appeler « L » ?", "Lawliet", "L Lawliet", "Ryuzaki")
q(A, "facile", "Quel Saiyan au grand cœur est le héros de Dragon Ball ?", "Son Goku", "Goku", "Sangoku")
q(A, "facile", "Quel prince des Saiyans est l'éternel rival de Goku ?", "Vegeta")
q(A, "moyen", "Quel dragon apparaît quand on réunit les boules de cristal de la Terre ?", "Shenron", "Shenlong")
q(A, "moyen", "Quel jeune homme veut exterminer tous les Titans dans L'Attaque des Titans ?", "Eren Jäger", "Eren", "Eren Yeager", "Eren Jaeger")
q(A, "facile", "Comment s'appelle la sœur de Tanjiro, transformée en démon ?", "Nezuko")
q(A, "facile", "Dans quel anime Yuji Itadori avale-t-il le doigt du démon Sukuna ?", "Jujutsu Kaisen", "JJK")
q(A, "moyen", "Quel exorciste aux yeux bandés est le plus puissant de Jujutsu Kaisen ?", "Satoru Gojo", "Gojo")
q(A, "facile", "Dans quel anime Izuku Midoriya hérite-t-il du pouvoir de All Might ?", "My Hero Academia", "Boku no Hero Academia", "MHA")
q(A, "moyen", "Dans quel anime les frères Elric cherchent-ils la pierre philosophale ?", "Fullmetal Alchemist", "FMA")
q(A, "facile", "Quel détective transformé en enfant résout des enquêtes avec des lunettes et un nœud papillon ?", "Détective Conan", "Conan", "Case Closed")
q(A, "moyen", "Dans quel anime Gon et Kirua passent-ils l'examen de chasseur ?", "Hunter x Hunter", "Hunter Hunter", "HxH")
q(A, "facile", "Quel héros chauve bat tous ses ennemis d'un seul coup de poing ?", "Saitama", "One Punch Man")
q(A, "moyen", "Dans quel anime de volley Hinata et Kageyama jouent-ils ensemble ?", "Haikyū", "Haikyu")
q(A, "facile", "Sous quel nom français connaît-on « Captain Tsubasa » ?", "Olive et Tom", "Captain Tsubasa")
q(A, "facile", "Quel robot géant, piloté par Actarus, était culte dans les années 80 en Algérie et en France ?", "Goldorak", "Grendizer", "Grandizer")
q(A, "moyen", "Dans quel anime Sung Jin-woo devient-il le chasseur le plus puissant du monde ?", "Solo Leveling")
q(A, "moyen", "Quelle magicienne elfe voyage après la mort du héros Himmel ?", "Frieren")
q(A, "moyen", "Dans quel anime Ichigo Kurosaki devient-il un shinigami remplaçant ?", "Bleach")
q(A, "moyen", "Dans quel anime Denji peut-il se transformer en homme-tronçonneuse ?", "Chainsaw Man")
q(A, "facile", "Dans quel anime un espion adopte-t-il Anya, une fillette télépathe ?", "Spy x Family", "Spy Family")
q(A, "moyen", "Dans quel anime Seiya et ses amis portent-ils des armures pour protéger Athéna ?", "Les Chevaliers du Zodiaque", "Chevaliers du zodiaque", "Saint Seiya")
q(A, "moyen", "Dans quel anime Lelouch obtient-il le pouvoir de donner des ordres absolus ?", "Code Geass")
q(A, "difficile", "Dans quel anime un micro-ondes modifié permet-il d'envoyer des messages dans le passé ?", "Steins;Gate", "Steins Gate")
q(A, "moyen", "Dans quel anime Ken Kaneki devient-il mi-humain mi-goule ?", "Tokyo Ghoul")
q(A, "moyen", "Dans quel anime de football un programme veut-il créer le meilleur attaquant du Japon ?", "Blue Lock")
q(A, "moyen", "Dans quel anime des orphelins découvrent-ils l'horrible secret de leur orphelinat ?", "The Promised Neverland", "Promised Neverland", "Yakusoku no Neverland")

json.dump(OUT, open("lot_texte_nov.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
print(len(OUT), Counter(x["categorie"] for x in OUT))
