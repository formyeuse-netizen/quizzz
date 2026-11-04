# -*- coding: utf-8 -*-
# Lot images n°2 (novembre 2026) : Algerie, voitures, espace, nature, sport, cuisine.
# Chaque candidat : [categorie, sous-type, reponse, [alias], difficulte, titre fr.wikipedia, titre en.wikipedia]
C = []
def a(cat, st, rep, al, dif, fr, en=None):
    C.append([cat, st, rep, al, dif, fr, en or ""])

# ---------------- ALGERIE : lieux ----------------
for rep, al, dif, fr, en in [
    ("Casbah d'Alger", ["casbah", "la casbah", "kasbah"], "facile", "Casbah d'Alger", "Casbah of Algiers"),
    ("Timgad", ["thamugadi"], "moyen", "Timgad", "Timgad"),
    ("Djémila", ["djemila", "cuicul"], "moyen", "Djémila", "Djémila"),
    ("Tipaza", ["tipasa", "ruines de tipaza"], "moyen", "Tipaza (site archéologique)", "Tipasa"),
    ("Tassili n'Ajjer", ["tassili", "tassili najjer"], "moyen", "Tassili n'Ajjer", "Tassili n'Ajjer"),
    ("Ghardaïa", ["ghardaia", "vallée du m'zab", "mzab", "m'zab"], "moyen", "Vallée du M'Zab", "M'zab"),
    ("Pont de Sidi M'Cid", ["sidi m'cid", "sidi mcid", "pont de constantine", "constantine"], "moyen", "Pont de Sidi M'Cid", "Sidi M'Cid Bridge"),
    ("Fort de Santa Cruz", ["santa cruz", "oran", "chapelle de santa cruz"], "moyen", "Fort de Santa Cruz (Oran)", "Santa Cruz Fort (Oran)"),
    ("Maqam Echahid", ["mémorial du martyr", "memorial du martyr", "maqam el chahid", "makam echahid"], "facile", "Mémorial du Martyr", "Maqam Echahid"),
    ("Grande Poste d'Alger", ["grande poste", "la grande poste"], "facile", "Grande Poste d'Alger", "Grande Poste d'Alger"),
    ("Tombeau de la Chrétienne", ["mausolée royal de maurétanie", "tombeau de la chretienne", "kbour er roumia"], "difficile", "Mausolée royal de Maurétanie", "Royal Mausoleum of Mauretania"),
    ("Medracen", ["imedghassen", "medghassen"], "difficile", "Medracen", "Medracen"),
    ("Kalâa des Béni Hammad", ["kalaa des beni hammad", "beni hammad", "qal'at beni hammad"], "difficile", "Kalâa des Béni Hammad", "Beni Hammad Fort"),
    ("Assekrem", ["hoggar", "ahaggar"], "difficile", "Assekrem", "Assekrem"),
    ("Taghit", [], "moyen", "Taghit", "Taghit"),
    ("Djurdjura", ["djudjura", "jurjura"], "moyen", "Djurdjura", "Djurdjura Mountains"),
    ("Cap Carbon", ["cap carbon bejaia"], "difficile", "Cap Carbon", "Cape Carbon"),
    ("Basilique Saint-Augustin", ["saint-augustin d'annaba", "basilique d'annaba", "annaba"], "moyen", "Basilique Saint-Augustin d'Annaba", "Basilica of St. Augustine"),
    ("Mansourah", ["mansourah tlemcen", "tlemcen"], "difficile", "Mansourah (Tlemcen)", "Mansourah, Tlemcen"),
    ("Mosquée Ketchaoua", ["ketchaoua", "djamaa ketchaoua"], "moyen", "Mosquée Ketchaoua", "Ketchaoua Mosque"),
    ("Jardin d'essai du Hamma", ["jardin d'essai", "hamma", "jardin d'essai d'alger"], "moyen", "Jardin d'essai du Hamma", "Jardin d'essai du Hamma"),
    ("Djanet", [], "difficile", "Djanet", "Djanet"),
    ("Timimoun", [], "difficile", "Timimoun", "Timimoun"),
    ("Pont Sidi Rached", ["sidi rached", "pont de constantine"], "difficile", "Pont Sidi Rached", "Sidi Rached Viaduct"),
    ("Mosquée Émir-Abdelkader", ["mosquee emir abdelkader", "mosquée de constantine", "emir abdelkader"], "moyen", "Mosquée Émir-Abdelkader", "Emir Abdelkader Mosque"),
    ("Palais des Raïs", ["bastion 23", "palais des rais"], "difficile", "Palais des Raïs", "Palais des Raïs"),
    ("Balcons de Ghoufi", ["ghoufi", "gorges de ghoufi"], "difficile", "Balcons de Ghoufi", "Ghoufi"),
    ("Hippone", ["hippo regius", "ruines d'hippone"], "difficile", "Hippone", "Hippo Regius"),
]:
    a("algerie", "lieu", rep, al, dif, fr, en)

# ---------------- ALGERIE : plats ----------------
for rep, al, dif, fr, en in [
    ("chakhchoukha", ["chakhchoukha", "chekhchoukha", "chakhchoukha biskria"], "moyen", "Chakhchoukha", "Chakhchoukha"),
    ("rechta", [], "moyen", "Rechta", "Rechta"),
    ("mhadjeb", ["mahjouba", "m'hadjeb", "mhajeb"], "facile", "Mhadjeb", "Mahjouba"),
    ("zlabia", ["zlebia", "jalebi", "zalabia"], "facile", "Zlabia", "Zalabia"),
    ("makrout", ["makroud", "maqrout"], "facile", "Makroud", "Makroudh"),
    ("garantita", ["karantika", "karantita", "calentica"], "moyen", "Karantika", "Karantita"),
    ("kesra", ["galette", "kessra", "matlou"], "moyen", "Kesra", "Kesra"),
    ("kalb el louz", ["qalb el louz", "chamia", "kalb ellouz"], "moyen", "Qalb el louz", "Qalb el louz"),
    ("berkoukes", ["berkoukes", "aiche", "aïch"], "difficile", "Berkoukes", "Berkoukes"),
    ("mesfouf", ["seffa", "mesfouf"], "difficile", "Mesfouf", "Mesfouf"),
    ("sfenj", ["sfendj", "beignet"], "moyen", "Sfenj", "Sfenj"),
    ("bourek", ["borek", "bourak", "brik"], "moyen", "Bourek", "Bourek"),
    ("chorba", ["chorba frik", "jari", "chorba beida"], "facile", "Chorba frik", "Chorba frik"),
    ("tamina", ["taknetta"], "difficile", "Tamina (pâtisserie)", "Tamina"),
    ("griwech", ["grioueche", "griouech", "chebakia"], "moyen", "Griwech", "Chebakia"),
    ("dziriette", ["dziriettes", "dziriate"], "difficile", "Dziriette", "Dziriette"),
    ("baklawa", ["baklava", "baklawa"], "facile", "Baklawa", None),
    ("dolma", ["dolmas"], "moyen", "Dolma", "Dolma"),
    ("lham lahlou", ["lham lahlou", "tajine lahlou", "tajine el ain"], "difficile", "Lham lahlou", "Lham lahlou"),
    ("trida", [], "difficile", "Trida", "Trida"),
]:
    if rep == "baklawa":
        continue   # deja dans la categorie cuisine
    a("algerie", "plat", rep, al, dif, fr, en)

# ---------------- ALGERIE : personnalites ----------------
for rep, al, dif, fr, en in [
    ("Émir Abdelkader", ["emir abdelkader", "abdelkader", "abd el kader", "abdelkader ibn muhieddine"], "facile", "Abd el-Kader", "Emir Abdelkader"),
    ("Abdelhamid Ben Badis", ["ben badis", "benbadis", "ibn badis"], "moyen", "Abdelhamid Ben Badis", "Abdelhamid Ben Badis"),
    ("Messali Hadj", ["messali"], "difficile", "Messali Hadj", "Messali Hadj"),
    ("Ahmed Ben Bella", ["ben bella", "benbella"], "moyen", "Ahmed Ben Bella", "Ahmed Ben Bella"),
    ("Houari Boumédiène", ["boumediene", "boumédiène", "houari boumediene"], "facile", "Houari Boumédiène", "Houari Boumediene"),
    ("Larbi Ben M'hidi", ["ben m'hidi", "ben mhidi", "larbi ben mhidi"], "moyen", "Larbi Ben M'hidi", "Larbi Ben M'hidi"),
    ("Mohamed Boudiaf", ["boudiaf"], "moyen", "Mohamed Boudiaf", "Mohamed Boudiaf"),
    ("Abdelaziz Bouteflika", ["bouteflika"], "facile", "Abdelaziz Bouteflika", "Abdelaziz Bouteflika"),
    ("Abdelmadjid Tebboune", ["tebboune"], "facile", "Abdelmadjid Tebboune", "Abdelmadjid Tebboune"),
    ("Kateb Yacine", ["kateb", "yacine kateb"], "moyen", "Kateb Yacine", "Kateb Yacine"),
    ("Assia Djebar", ["djebar"], "difficile", "Assia Djebar", "Assia Djebar"),
    ("Mohammed Dib", ["dib", "mohamed dib"], "difficile", "Mohammed Dib", "Mohammed Dib"),
    ("Hassiba Ben Bouali", ["ben bouali", "hassiba"], "difficile", "Hassiba Ben Bouali", "Hassiba Ben Bouali"),
    ("Djamila Bouhired", ["bouhired"], "moyen", "Djamila Bouhired", "Djamila Bouhired"),
    ("Krim Belkacem", ["belkacem krim", "krim"], "difficile", "Krim Belkacem", "Krim Belkacem"),
    ("Ferhat Abbas", ["abbas"], "difficile", "Ferhat Abbas", "Ferhat Abbas"),
    ("Mostefa Ben Boulaïd", ["ben boulaid", "mostefa ben boulaid", "mustapha ben boulaid"], "difficile", "Mostefa Ben Boulaïd", "Mostefa Ben Boulaïd"),
    ("Didouche Mourad", ["didouche"], "difficile", "Didouche Mourad", "Didouche Mourad"),
    ("Hocine Aït Ahmed", ["ait ahmed", "aït ahmed", "hocine ait ahmed"], "difficile", "Hocine Aït Ahmed", "Hocine Aït Ahmed"),
    ("Abane Ramdane", ["abane", "ramdane abane"], "difficile", "Abane Ramdane", "Abane Ramdane"),
    ("Lalla Fatma N'Soumer", ["fatma n'soumer", "fatma nsoumer", "lalla fatma"], "moyen", "Lalla Fatma N'Soumer", "Lalla Fatma N'Soumer"),
    ("Ali la Pointe", ["ali ammar"], "moyen", "Ali la Pointe", "Ali La Pointe"),
    ("Rabah Madjer", ["madjer"], "moyen", "Rabah Madjer", "Rabah Madjer"),
    ("Lakhdar Belloumi", ["belloumi"], "difficile", "Lakhdar Belloumi", "Lakhdar Belloumi"),
]:
    a("algerie", "perso", rep, al, dif, fr, en)

# ---------------- VOITURES ----------------
for rep, al, dif, fr, en in [
    ("renault symbol", ["symbol", "renault symbole", "thalia"], "facile", "Renault Symbol", "Renault Symbol"),
    ("dacia logan", ["logan"], "facile", "Dacia Logan", "Dacia Logan"),
    ("dacia sandero", ["sandero"], "facile", "Dacia Sandero", "Dacia Sandero"),
    ("peugeot 206", ["206"], "facile", "Peugeot 206", "Peugeot 206"),
    ("peugeot 404", ["404"], "moyen", "Peugeot 404", "Peugeot 404"),
    ("peugeot 504", ["504"], "moyen", "Peugeot 504", "Peugeot 504"),
    ("toyota hilux", ["hilux"], "moyen", "Toyota Hilux", "Toyota Hilux"),
    ("toyota land cruiser", ["land cruiser", "station"], "moyen", "Toyota Land Cruiser", "Toyota Land Cruiser"),
    ("nissan patrol", ["patrol"], "moyen", "Nissan Patrol", "Nissan Patrol"),
    ("mercedes classe g", ["classe g", "g class", "mercedes g", "g-wagon", "g wagon"], "moyen", "Mercedes-Benz Classe G", "Mercedes-Benz G-Class"),
    ("range rover", [], "moyen", "Range Rover", "Range Rover"),
    ("lancia stratos", ["stratos"], "difficile", "Lancia Stratos", "Lancia Stratos"),
    ("lamborghini urus", ["urus"], "moyen", "Lamborghini Urus", "Lamborghini Urus"),
    ("pagani zonda", ["zonda"], "difficile", "Pagani Zonda", "Pagani Zonda"),
    ("bmw m3", ["m3"], "moyen", "BMW M3", "BMW M3"),
    ("mitsubishi lancer evolution", ["lancer evolution", "lancer evo", "evo"], "difficile", "Mitsubishi Lancer Evolution", "Mitsubishi Lancer Evolution"),
    ("subaru impreza", ["impreza", "impreza wrx", "subaru wrx"], "moyen", "Subaru Impreza", "Subaru Impreza"),
    ("smart fortwo", ["smart"], "facile", "Smart Fortwo", "Smart Fortwo"),
    ("citroën méhari", ["mehari", "méhari", "citroen mehari"], "difficile", "Citroën Méhari", "Citroën Méhari"),
    ("citroën traction avant", ["traction avant", "traction", "citroen traction"], "moyen", "Citroën Traction Avant", "Citroën Traction Avant"),
    ("chevrolet corvette", ["corvette"], "moyen", "Chevrolet Corvette C2", "Chevrolet Corvette (C2)"),
    ("cadillac eldorado", ["eldorado", "cadillac"], "difficile", "Cadillac Eldorado", "Cadillac Eldorado"),
    ("ford f-150", ["f-150", "f150", "ford f150"], "moyen", "Ford F-150", "Ford F-150"),
    ("tesla model 3", ["model 3"], "moyen", "Tesla Model 3", "Tesla Model 3"),
    ("toyota prius", ["prius"], "moyen", "Toyota Prius", "Toyota Prius"),
    ("toyota corolla", ["corolla"], "moyen", "Toyota Corolla", "Toyota Corolla"),
    ("renault espace", ["espace"], "moyen", "Renault Espace", "Renault Espace"),
    ("volkswagen polo", ["polo", "vw polo"], "moyen", "Volkswagen Polo", "Volkswagen Polo"),
    ("fiat uno", ["uno"], "moyen", "Fiat Uno", "Fiat Uno"),
    ("koenigsegg agera", ["agera", "koenigsegg"], "difficile", "Koenigsegg Agera", "Koenigsegg Agera"),
    ("porsche cayenne", ["cayenne"], "moyen", "Porsche Cayenne", "Porsche Cayenne"),
    ("ferrari laferrari aperta", [], "difficile", None, None),
]:
    if fr is None:
        continue
    a("voitures", "voiture", rep, al, dif, fr, en)

# ---------------- ESPACE ----------------
for rep, al, dif, fr, en in [
    ("nébuleuse du Crabe", ["crabe", "nebuleuse du crabe", "crab nebula", "m1"], "difficile", "Nébuleuse du Crabe", "Crab Nebula"),
    ("Pléiades", ["pleiades", "les pléiades", "m45", "amas des pléiades"], "difficile", "Pléiades (astronomie)", "Pleiades"),
    ("constellation d'Orion", ["orion"], "difficile", "Orion (constellation)", "Orion (constellation)"),
    ("Grande Ourse", ["grande ourse", "big dipper", "grand chariot", "casserole"], "moyen", "Grand Chariot", "Big Dipper"),
    ("fusée Ariane 5", ["ariane", "ariane 5", "ariane 6"], "moyen", "Ariane 5", "Ariane 5"),
    ("station Mir", ["mir"], "difficile", "Mir (station spatiale)", "Mir"),
    ("étoile filante", ["météore", "meteore", "meteor", "shooting star"], "moyen", "Météore", "Meteoroid"),
    ("météorite", ["meteorite", "meteorite"], "moyen", "Météorite", "Meteorite"),
    ("radiotélescope", ["radiotelescope", "radio telescope", "antenne"], "difficile", "Very Large Array", "Very Large Array"),
    ("Apollo 11", ["apollo", "premier pas sur la lune"], "moyen", "Apollo 11", "Apollo 11"),
    ("Youri Gagarine", ["gagarine", "gagarin", "yuri gagarin"], "moyen", "Youri Gagarine", "Yuri Gagarin"),
    ("Neil Armstrong", ["armstrong"], "facile", "Neil Armstrong", "Neil Armstrong"),
    ("Valentina Terechkova", ["terechkova", "tereshkova"], "difficile", "Valentina Terechkova", "Valentina Tereshkova"),
    ("Thomas Pesquet", ["pesquet"], "moyen", "Thomas Pesquet", "Thomas Pesquet"),
    ("Laïka", ["laika"], "moyen", "Laïka", "Laika"),
    ("anneaux de Saturne", ["anneaux", "rings of saturn"], "moyen", "Anneaux de Saturne", "Rings of Saturn"),
    ("Olympus Mons", ["olympus mons", "mont olympe (mars)"], "difficile", "Olympus Mons", "Olympus Mons"),
    ("lune de sang", ["éclipse lunaire", "eclipse lunaire", "lunar eclipse", "blood moon"], "moyen", "Éclipse lunaire", "Lunar eclipse"),
    ("nébuleuse de la Tête de Cheval", ["tête de cheval", "tete de cheval", "horsehead"], "difficile", "Nébuleuse de la Tête de Cheval", "Horsehead Nebula"),
    ("lever de Terre", ["earthrise", "lever de terre"], "difficile", "Earthrise", "Earthrise"),
]:
    a("espace", "objet", rep, al, dif, fr, en)

# ---------------- NATURE ----------------
for rep, al, dif, fr, en in [
    ("Lac Titicaca", ["titicaca"], "moyen", "Lac Titicaca", "Lake Titicaca"),
    ("Mont Ararat", ["ararat"], "difficile", "Mont Ararat", "Mount Ararat"),
    ("Tre Cime di Lavaredo", ["tre cime", "dolomites", "trois cimes de lavaredo"], "difficile", "Tre Cime di Lavaredo", "Tre Cime di Lavaredo"),
    ("Cascades d'Ouzoud", ["ouzoud", "chutes d'ouzoud"], "difficile", "Cascades d'Ouzoud", "Ouzoud Falls"),
    ("Calanques de Marseille", ["calanques", "calanque"], "moyen", "Massif des Calanques", "Calanques"),
    ("Falaises d'Étretat", ["étretat", "etretat", "aiguille d'étretat"], "moyen", "Falaises d'Étretat", "Étretat"),
    ("Dune du Pilat", ["pilat", "dune du pyla", "pyla"], "moyen", "Dune du Pilat", "Dune of Pilat"),
    ("Lac de Bled", ["bled", "lac bled"], "difficile", "Lac de Bled", "Lake Bled"),
    ("Lac Louise", ["lake louise"], "difficile", "Lac Louise", "Lake Louise"),
    ("Mont Roraima", ["roraima"], "difficile", "Mont Roraima", "Mount Roraima"),
    ("Kīlauea", ["kilauea", "volcan d'hawaï"], "difficile", "Kīlauea", "Kīlauea"),
    ("Strokkur", ["geysir", "geyser islandais"], "difficile", "Strokkur", "Strokkur"),
    ("Îles Lofoten", ["lofoten"], "difficile", "Îles Lofoten", "Lofoten"),
    ("Delicate Arch", ["arches", "arches national park", "arche délicate"], "difficile", "Delicate Arch", "Delicate Arch"),
    ("Grottes de Waitomo", ["waitomo", "grotte aux vers luisants"], "difficile", "Grottes de Waitomo", "Waitomo Glowworm Caves"),
    ("Hang Sơn Đoòng", ["son doong", "hang son doong"], "difficile", "Hang Sơn Đoòng", "Hang Sơn Đoòng"),
    ("Lençóis Maranhenses", ["lencois maranhenses", "lençois"], "difficile", "Parc national des Lençóis Maranhenses", "Lençóis Maranhenses National Park"),
    ("Douze Apôtres", ["twelve apostles", "12 apotres", "douze apotres"], "difficile", "Douze Apôtres", "The Twelve Apostles (Victoria)"),
    ("Lac Retba", ["lac rose", "retba"], "moyen", "Lac Rose", "Lake Retba"),
    ("Désert blanc", ["desert blanc", "white desert"], "difficile", "Désert blanc", "White Desert National Park"),
    ("Dallol", ["danakil", "dépression du danakil"], "difficile", "Dallol (volcan)", "Dallol (hydrothermal system)"),
    ("Mont Kailash", ["kailash"], "difficile", "Mont Kailash", "Mount Kailash"),
    ("Chutes de Kaieteur", ["kaieteur"], "difficile", "Chutes de Kaieteur", "Kaieteur Falls"),
    ("Grotte de Fingal", ["fingal", "fingal's cave"], "difficile", "Grotte de Fingal", "Fingal's Cave"),
    ("Oasis de Siwa", ["siwa"], "difficile", "Siwa", "Siwa Oasis"),
    ("Mont Cook", ["aoraki", "aoraki mont cook"], "difficile", "Aoraki / Mont Cook", "Aoraki / Mount Cook"),
    ("Annapurna", [], "difficile", "Annapurna", "Annapurna"),
    ("Mer de glace", ["mer de glace chamonix"], "difficile", "Mer de Glace", "Mer de Glace"),
]:
    a("nature", "lieu", rep, al, dif, fr, en)

# ---------------- SPORT : sportifs ----------------
for rep, al, dif, fr, en in [
    ("Taoufik Makhloufi", ["makhloufi"], "moyen", "Taoufik Makhloufi", "Taoufik Makhloufi"),
    ("Noureddine Morceli", ["morceli"], "moyen", "Noureddine Morceli", "Noureddine Morceli"),
    ("Hassiba Boulmerka", ["boulmerka"], "moyen", "Hassiba Boulmerka", "Hassiba Boulmerka"),
    ("Kaylia Nemour", ["nemour"], "moyen", "Kaylia Nemour", "Kaylia Nemour"),
    ("Hicham El Guerrouj", ["el guerrouj", "guerrouj"], "moyen", "Hicham El Guerrouj", "Hicham El Guerrouj"),
    ("Carl Lewis", ["lewis"], "moyen", "Carl Lewis", "Carl Lewis"),
    ("Michael Johnson", [], "difficile", "Michael Johnson (athlétisme)", "Michael Johnson (sprinter)"),
    ("Florence Griffith-Joyner", ["flo-jo", "griffith joyner", "florence griffith joyner"], "difficile", "Florence Griffith-Joyner", "Florence Griffith Joyner"),
    ("Eliud Kipchoge", ["kipchoge"], "moyen", "Eliud Kipchoge", "Eliud Kipchoge"),
    ("Mo Farah", ["farah", "mohamed farah"], "moyen", "Mo Farah", "Mo Farah"),
    ("Kenenisa Bekele", ["bekele"], "difficile", "Kenenisa Bekele", "Kenenisa Bekele"),
    ("Armand Duplantis", ["duplantis", "mondo duplantis", "mondo"], "moyen", "Armand Duplantis", "Armand Duplantis"),
    ("Simone Biles", ["biles"], "facile", "Simone Biles", "Simone Biles"),
    ("Nadia Comăneci", ["comaneci", "nadia comaneci"], "moyen", "Nadia Comăneci", "Nadia Comăneci"),
    ("Teddy Riner", ["riner"], "facile", "Teddy Riner", "Teddy Riner"),
    ("Nikola Karabatić", ["karabatic", "nikola karabatic"], "moyen", "Nikola Karabatić", "Nikola Karabatić"),
    ("Michael Phelps", ["phelps"], "facile", "Michael Phelps", "Michael Phelps"),
    ("Katie Ledecky", ["ledecky"], "difficile", "Katie Ledecky", "Katie Ledecky"),
    ("Léon Marchand", ["leon marchand", "marchand"], "moyen", "Léon Marchand", "Léon Marchand"),
    ("Tiger Woods", ["woods", "tiger"], "facile", "Tiger Woods", "Tiger Woods"),
    ("Canelo Álvarez", ["canelo", "canelo alvarez", "saul alvarez"], "moyen", "Saúl Álvarez", "Canelo Álvarez"),
    ("Khabib Nurmagomedov", ["khabib", "nurmagomedov"], "moyen", "Khabib Nurmagomedov", "Khabib Nurmagomedov"),
    ("Francis Ngannou", ["ngannou"], "moyen", "Francis Ngannou", "Francis Ngannou"),
    ("Valentino Rossi", ["rossi"], "moyen", "Valentino Rossi", "Valentino Rossi"),
    ("Marc Márquez", ["marquez", "marc marquez"], "difficile", "Marc Márquez", "Marc Márquez"),
    ("Sébastien Loeb", ["loeb"], "moyen", "Sébastien Loeb", "Sébastien Loeb"),
    ("Max Verstappen", ["verstappen"], "facile", "Max Verstappen", "Max Verstappen"),
    ("Mikaela Shiffrin", ["shiffrin"], "difficile", "Mikaela Shiffrin", "Mikaela Shiffrin"),
    ("Wayne Gretzky", ["gretzky"], "difficile", "Wayne Gretzky", "Wayne Gretzky"),
    ("Tom Brady", ["brady"], "moyen", "Tom Brady", "Tom Brady"),
    ("Virat Kohli", ["kohli"], "difficile", "Virat Kohli", "Virat Kohli"),
    ("Magnus Carlsen", ["carlsen"], "moyen", "Magnus Carlsen", "Magnus Carlsen"),
    ("Coco Gauff", ["gauff"], "moyen", "Coco Gauff", "Coco Gauff"),
    ("Aryna Sabalenka", ["sabalenka"], "moyen", "Aryna Sabalenka", "Aryna Sabalenka"),
    ("Daniil Medvedev", ["medvedev"], "moyen", "Daniil Medvedev", "Daniil Medvedev"),
    ("Tony Hawk", ["hawk"], "moyen", "Tony Hawk", "Tony Hawk"),
    ("Kelly Slater", ["slater"], "difficile", "Kelly Slater", "Kelly Slater"),
    ("Tadej Pogačar", [], "difficile", None, None),
]:
    if fr is None:
        continue
    a("sport", "perso", rep, al, dif, fr, en)

# ---------------- CUISINE : plats du monde ----------------
for rep, al, dif, fr, en in [
    ("feijoada", [], "difficile", "Feijoada", "Feijoada"),
    ("jollof", ["riz jollof", "jollof rice"], "moyen", "Riz jollof", "Jollof rice"),
    ("injera", [], "difficile", "Injera", "Injera"),
    ("pastilla", ["bastilla", "bstilla"], "moyen", "Pastilla", "Pastilla"),
    ("harira", [], "moyen", "Harira", "Harira"),
    ("mansaf", [], "difficile", "Mansaf", "Mansaf"),
    ("kabsa", ["machboos"], "difficile", "Kabsa", "Kabsa"),
    ("koshari", ["kochari", "koshary"], "difficile", "Koshari", "Koshary"),
    ("lahmacun", ["pizza turque", "lahmajoun"], "moyen", "Lahmacun", "Lahmacun"),
    ("simit", [], "difficile", "Simit", "Simit"),
    ("goulash", ["goulasch", "gulyas"], "moyen", "Goulash", "Goulash"),
    ("pelmeni", [], "difficile", "Pelmeni", "Pelmeni"),
    ("blinis", ["blini"], "moyen", "Blini", "Blini"),
    ("tortilla espagnole", ["tortilla", "spanish omelette"], "moyen", "Tortilla de patatas", "Spanish omelette"),
    ("patatas bravas", ["bravas"], "moyen", "Patatas bravas", "Patatas bravas"),
    ("chili con carne", ["chili"], "moyen", "Chili con carne", "Chili con carne"),
    ("mac and cheese", ["macaroni au fromage", "macaroni and cheese", "mac & cheese"], "facile", "Macaroni and cheese", "Macaroni and cheese"),
    ("apple pie", ["tarte aux pommes"], "moyen", "Tarte aux pommes", "Apple pie"),
    ("cupcake", ["cupcakes"], "facile", "Cupcake", "Cupcake"),
    ("muffin", ["muffins"], "facile", "Muffin", "Muffin"),
    ("soupe à l'oignon", ["soupe a l'oignon", "onion soup"], "moyen", "Soupe à l'oignon", "French onion soup"),
    ("bouillabaisse", [], "moyen", "Bouillabaisse", "Bouillabaisse"),
    ("cassoulet", [], "moyen", "Cassoulet", "Cassoulet"),
    ("choucroute", ["choucroute garnie", "sauerkraut"], "moyen", "Choucroute garnie", "Choucroute garnie"),
    ("bœuf bourguignon", ["boeuf bourguignon", "bourguignon"], "moyen", "Bœuf bourguignon", "Beef bourguignon"),
    ("profiteroles", ["profiterole"], "moyen", "Profiterole", "Profiterole"),
    ("paris-brest", ["paris brest"], "difficile", "Paris-brest", "Paris–Brest"),
    ("forêt-noire", ["foret noire", "forêt noire", "black forest"], "moyen", "Forêt-noire (gâteau)", "Black Forest gateau"),
    ("strudel", ["apfelstrudel", "strudel aux pommes"], "moyen", "Apfelstrudel", "Apple strudel"),
    ("pastel de nata", ["pasteis de nata", "pastel de belém"], "moyen", "Pastel de nata", "Pastel de nata"),
    ("arancini", ["arancino"], "difficile", "Arancini", "Arancini"),
    ("bruschetta", [], "moyen", "Bruschetta", "Bruschetta"),
    ("minestrone", [], "difficile", "Minestrone", "Minestrone"),
    ("gelato", ["glace italienne"], "facile", "Gelato", "Gelato"),
    ("xiaolongbao", ["xiao long bao"], "difficile", "Xiaolongbao", "Xiaolongbao"),
    ("hot pot", ["fondue chinoise", "huoguo"], "moyen", "Fondue chinoise", "Hot pot"),
    ("laksa", [], "difficile", "Laksa", "Laksa"),
    ("nasi goreng", [], "moyen", "Nasi goreng", "Nasi goreng"),
    ("satay", ["saté", "sate"], "moyen", "Saté", "Satay"),
    ("tom yum", ["tom yam"], "moyen", "Tom yam", "Tom yum"),
    ("dosa", ["dossa"], "difficile", "Dosa", "Dosa"),
    ("poulet tandoori", ["tandoori", "tandoori chicken"], "moyen", "Poulet tandoori", "Tandoori chicken"),
    ("momos", ["momo"], "difficile", "Momo (cuisine)", "Momo (food)"),
    ("udon", [], "moyen", "Udon", "Udon"),
    ("tteokbokki", ["topokki", "tteok-bokki"], "difficile", "Tteokbokki", "Tteok-bokki"),
    ("bulgogi", [], "difficile", "Bulgogi", "Bulgogi"),
]:
    a("cuisine", "plat", rep, al, dif, fr, en)

import json
json.dump(C, open("candidats_img_nov2.json", "w", encoding="utf-8"), ensure_ascii=False)
if __name__ == "__main__":
    from collections import Counter
    print(len(C), Counter(c[0] for c in C))
