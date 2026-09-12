# -*- coding: utf-8 -*-
"""Ajoute des alias anglais aux reponses, rend les questions capitales bilingues,
et retire Israel. Idempotent : relançable sans dupliquer."""
import json, glob, re, sys
sys.path.insert(0, '.')
from matching import normaliser as N

aug = json.load(open('/tmp/aug_pays.json'))
CMAP = {k: set(v) for k, v in aug['cmap'].items()}      # norm(pays fr) -> alias
CAPMAP = {k: set(v) for k, v in aug['capmap'].items()}  # norm(capitale fr) -> alias
FR2EN = aug['fr2en']                                    # norm(pays fr) -> nom EN

TRAD = {}
TRAD['animaux'] = {
 'abeille':['bee'],'addax':['addax'],'aigle royal':['golden eagle','eagle'],'alpaga':['alpaca'],
 'anchois':['anchovy'],'anguille':['eel'],'ara':['macaw'],'aurochs':['aurochs'],
 'baleine bleue':['blue whale'],'bar':['sea bass','bass'],'belette':['weasel'],'bison':['bison'],
 'bongo':['bongo'],'brochet':['pike'],'buffle':['buffalo'],'béluga':['beluga'],
 'cachalot':['sperm whale'],'canard colvert':['mallard','duck'],'castor':['beaver'],
 'cerf':['deer','stag'],'chacal':['jackal'],'chameau de bactriane':['bactrian camel','camel'],
 'chamois':['chamois'],'chat sauvage':['wildcat'],'cheval':['horse'],'chimpanzé':['chimpanzee','chimp'],
 'chouette hulotte':['tawny owl','owl'],'chèvre':['goat'],'cigogne':['stork'],
 'cobra royal':['king cobra','cobra'],'coccinelle':['ladybug','ladybird'],'cochon':['pig'],
 'coq':['rooster','cock'],'corbeau':['raven','crow'],'coyote':['coyote'],'crapaud':['toad'],
 'crocodile':['crocodile'],'cygne':['swan'],'daim':['fallow deer'],'diable de tasmanie':['tasmanian devil'],
 'doryphore':['colorado potato beetle'],'dromadaire':['dromedary','camel'],'dugong':['dugong'],
 'espadon':['swordfish'],'faucon pèlerin':['peregrine falcon','falcon'],'fennec':['fennec fox','fennec'],
 'flamant rose':['flamingo'],'fou de bassan':['gannet'],'fouine':['beech marten','marten'],
 'frelon asiatique':['asian hornet','hornet'],'gazelle':['gazelle'],'girafe':['giraffe'],
 'gnou':['gnu','wildebeest'],'gorille':['gorilla'],'grand dauphin':['bottlenose dolphin','dolphin'],
 'grand tétras':['capercaillie'],"grand-duc d'europe":['eurasian eagle-owl','eagle owl'],
 'grenouille':['frog'],'guépard':['cheetah'],'hareng':['herring'],'hippocampe':['seahorse'],
 'hippopotame':['hippopotamus','hippo'],'homard':['lobster'],'hyène tachetée':['spotted hyena','hyena'],
 'hérisson':['hedgehog'],'héron':['heron'],'impala':['impala'],'jaguar':['jaguar'],
 'kangourou':['kangaroo'],'koala':['koala'],'lama':['llama'],'lamantin':['manatee'],
 'langoustine':['langoustine','scampi'],'lapin':['rabbit'],'lion':['lion'],'loup':['wolf'],
 'loup à crinière':['maned wolf'],'loutre':['otter'],'lycaon':['african wild dog'],'lynx':['lynx'],
 'lynx roux':['bobcat'],'léopard':['leopard'],'magot':['barbary macaque'],
 'manchot empereur':['emperor penguin','penguin'],'mandrill':['mandrill'],'maquereau':['mackerel'],
 'marsouin':['porpoise'],'monarque':['monarch butterfly','monarch'],'morse':['walrus'],'morue':['cod'],
 'mouton':['sheep'],'ocelot':['ocelot'],'okapi':['okapi'],'ornithorynque':['platypus'],
 'orque':['orca','killer whale'],'otarie':['sea lion'],'ours blanc':['polar bear'],
 'ours brun':['brown bear'],'ours noir':['black bear'],'ours à lunettes':['spectacled bear'],
 'panda géant':['giant panda','panda'],'panda roux':['red panda'],'paon':['peacock'],
 'paresseux':['sloth'],'patas':['patas monkey'],'perche':['perch'],
 'perruche ondulée':['budgerigar','budgie'],'phoque':['seal'],'pieuvre':['octopus'],
 'poisson rouge':['goldfish'],'poisson-lune':['sunfish','ocean sunfish'],
 'puma':['puma','cougar','mountain lion'],'putois':['polecat'],
 'pygargue à tête blanche':['bald eagle'],'pélican':['pelican'],'raie manta':['manta ray','manta'],
 'ratel':['honey badger'],'raton laveur':['raccoon'],'renard':['fox'],'renne':['reindeer','caribou'],
 'requin blanc':['great white shark','white shark'],'requin grande gueule':['megamouth shark'],
 'rhinocéros':['rhinoceros','rhino'],'salamandre':['salamander'],'sanglier':['wild boar','boar'],
 'saola':['saola'],'sardine':['sardine'],'saumon':['salmon'],'saïga':['saiga'],'suricate':['meerkat'],
 'tamanoir':['giant anteater','anteater'],'tanuki':['raccoon dog','tanuki'],'tatou':['armadillo'],
 'thon albacore':['yellowfin tuna','tuna'],'tigre':['tiger'],'tortue géante':['giant tortoise','tortoise'],
 'tortue luth':['leatherback turtle','leatherback','turtle'],'toucan':['toucan'],
 'triton crêté':['crested newt','newt'],'truite':['trout'],'vache':['cow'],'veuve noire':['black widow'],
 'vigogne':['vicuna'],'wombat':['wombat'],'yak':['yak'],'zèbre':['zebra'],'âne':['donkey'],
 'écureuil':['squirrel'],'élan':['moose','elk'],"éléphant d'afrique":['african elephant','elephant'],
 "éléphant d'asie":['asian elephant','elephant'],
}
TRAD['aliments'] = {
 'abricot':['apricot'],'ail':['garlic'],'ananas':['pineapple'],'artichaut':['artichoke'],
 'asperge':['asparagus'],'aubergine':['eggplant','aubergine'],'banane':['banana'],'brocoli':['broccoli'],
 'carotte':['carrot'],'cerise':['cherry'],'chou':['cabbage'],'chou-fleur':['cauliflower'],
 'citron':['lemon'],'citrouille':['pumpkin'],'clémentine':['clementine'],'concombre':['cucumber'],
 'datte':['date'],'figue':['fig'],'fraise':['strawberry'],'framboise':['raspberry'],
 'groseille':['currant','redcurrant'],'haricot vert':['green bean'],'kaki':['persimmon'],'kiwi':['kiwi'],
 'laitue':['lettuce'],'litchi':['lychee'],'mangue':['mango'],'maïs':['corn','maize'],'melon':['melon'],
 'myrtille':['blueberry'],'navet':['turnip'],'noix de coco':['coconut'],'oignon':['onion'],
 'orange':['orange'],'pamplemousse':['grapefruit'],'papaye':['papaya'],'pastèque':['watermelon'],
 'patate douce':['sweet potato'],'petit pois':['pea','peas','green pea'],'poire':['pear'],
 'poivron':['bell pepper','pepper'],'pomme':['apple'],'pomme de terre':['potato'],'prune':['plum'],
 'pêche':['peach'],'radis':['radish'],'raisin':['grape','grapes'],'tomate':['tomato'],'épinard':['spinach'],
}
TRAD['langues'] = {
 'albanais':['albanian'],'allemand':['german'],'amharique':['amharic'],'anglais':['english'],
 'arabe':['arabic'],'arménien':['armenian'],'basque':['basque'],'bengali':['bengali'],
 'chinois':['chinese','mandarin'],'coréen':['korean'],'espagnol':['spanish'],'espéranto':['esperanto'],
 'finnois':['finnish'],'français':['french'],'grec':['greek'],'géorgien':['georgian'],
 'hawaïen':['hawaiian'],'hindi':['hindi'],'hongrois':['hungarian'],'hébreu':['hebrew'],
 'indonésien':['indonesian'],'irlandais':['irish','gaelic'],'italien':['italian'],'japonais':['japanese'],
 'latin':['latin'],'néerlandais':['dutch'],'philippin':['filipino','tagalog'],'polonais':['polish'],
 'portugais':['portuguese'],'roumain':['romanian'],'russe':['russian'],'suédois':['swedish'],
 'swahili':['swahili'],'tamoul':['tamil'],'tchèque':['czech'],'thaï':['thai'],'turc':['turkish'],
 'vietnamien':['vietnamese'],'zoulou':['zulu'],
}
TRAD['corps'] = {
 'bassin':['pelvis'],'cage thoracique':['rib cage','ribcage'],'cerveau':['brain'],
 'colonne vertébrale':['spine','spinal column','vertebral column'],'crâne':['skull'],'cœur':['heart'],
 'dent':['tooth'],'foie':['liver'],'fémur':['femur','thigh bone'],'gros intestin':['large intestine','colon'],
 'intestin grêle':['small intestine'],'main':['hand'],'poumons':['lungs','lung'],
 'rein':['kidney','kidneys'],'rotule':['kneecap','patella'],'squelette':['skeleton'],'œil':['eye'],
 'œsophage':['esophagus','oesophagus','gullet'],
}
TRAD_N = {cat: {N(k): v for k, v in d.items()} for cat, d in TRAD.items()}

def merge(entry, extra):
    al = list(entry.get('alias') or [])
    seen = {N(a) for a in al}
    seen.add(N(entry['reponse']))
    for x in extra:
        if x and N(x) not in seen:
            al.append(x); seen.add(N(x))
    entry['alias'] = al

DRY = '--apply' not in sys.argv
report = {}
manquants = {c: [] for c in TRAD}
for f in sorted(glob.glob('lot*.json')):
    try: d = json.load(open(f))
    except: continue
    if not isinstance(d, list): continue
    garde = []; removed = 0; touched = 0
    for e in d:
        if not isinstance(e, dict): garde.append(e); continue
        rep = e.get('reponse', ''); cat = e.get('categorie', ''); q = e.get('question', '')
        # --- retrait Israel ---
        if N(rep) == N('Israël') or re.search(r'capitale de\s*:\s*isra', q, re.I) \
           or 'israël' in q.lower() or 'israel' in q.lower():
            removed += 1; continue
        before = list(e.get('alias') or [])
        # --- pays / capitales (toutes categories) ---
        if N(rep) in CMAP: merge(e, CMAP[N(rep)])
        if N(rep) in CAPMAP: merge(e, CAPMAP[N(rep)])
        # --- question capitale bilingue ---
        m = re.search(r'(capitale de\s*:\s*)(.+?)(\s*\?)', q)
        if m:
            pays_fr = m.group(2).strip(); en = FR2EN.get(N(pays_fr))
            if en and N(en) != N(pays_fr) and '(' not in q:
                e['question'] = f"{m.group(1)}{pays_fr} ({en}){m.group(3)}"
        # --- categories a noms communs ---
        if cat in TRAD_N:
            tr = TRAD_N[cat].get(N(rep))
            if tr: merge(e, tr)
            else: manquants[cat].append(rep)
        if list(e.get('alias') or []) != before or (m and e['question'] != q):
            touched += 1
        garde.append(e)
    report[f] = (len(d), removed, touched)
    if not DRY:
        json.dump(garde, open(f, 'w'), ensure_ascii=False, indent=1)

print('MODE', 'DRY (rien ecrit)' if DRY else 'APPLIQUE')
for f, (n, rm, tc) in report.items():
    if rm or tc: print(f'{f}: {n} entrees, {rm} Israel retirees, {tc} enrichies')
for c, miss in manquants.items():
    miss = sorted(set(miss))
    if miss: print(f'!! {c} sans traduction:', miss)
