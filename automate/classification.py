from config import ARTICLES, PREP, NLIEU, TITRES
from normalisation import norm

# -----------------------------------------------------------------------
# Verbes de parole et d'action (complement de verbs.json)
# -----------------------------------------------------------------------
SPEECH_VERBS = frozenset("""
    dit repondit demanda reprit declara affirma nia cria murmura chuchota
    recria objecta intervint protesta acquiesca remarqua ajouta continua
    interrompit admit reconnut conceda expliqua precisa ordonna pria
    sugera proposa promit gronda bougonna balbutia hesita hurla appela
    interpella salua remercia reprocha accusa constata observa nota
    releva rapporta avoua confia glissa insinua soupira ricana grommela
    bredouilla retorqua repliqua insista prevint avertit lanca souffla
    chuchota susurra marmonna bafouilla grogna soupira laissa echapper
    epliqua reconnut comprit vit sentit pensa crut remarqua trouva
    s exclama s ecria s interrogea s etonna s inquieta
""".split())

# Verbes indiquant qu'un lieu suit ou que le sujet se deplace
PLACE_VERBS = frozenset("""
    alla allait allaient ira iront arriva arrivait vint venait
    partirent partait repartit retourna revint rejoignit
    traversait traversa visitait visita quittait quitta atteignit
    habita habitait residait sejourna conduisit mena amena emmena
    dirigea entrait sortit trouva situa trouvait se trouve situe
    venait habitait vivait
""".split())

# Prepositions "de" et variantes : indicatrices de lieu SEULEMENT
# si le mot qui precede est lui-meme un nom de lieu (p2 in NLIEU)
_DE_PREPS = frozenset({"de", "du", "des", "d"})


def classer_candidat(nom, mots, debut, pos, verbes):
    k, N = len(nom), len(mots)
    milieu = pers = lieu = art = 0

    tous_verbes_pers = verbes | SPEECH_VERBS
    tous_verbes_lieu = verbes | PLACE_VERBS

    for i in pos.get(nom[0], []):
        if tuple(mots[i:i+k]) != nom or debut[i]:
            continue
        milieu += 1

        # Contexte : 3 mots avant, 2 mots apres (sans franchir de frontiere)
        pv  = norm(mots[i-1]) if i > 0 else ""
        p2  = norm(mots[i-2]) if i > 1 and not debut[i-1] else ""
        p3  = norm(mots[i-3]) if i > 2 and not debut[i-1] and not debut[i-2] else ""
        nx  = norm(mots[i+k])   if i+k < N and not debut[i+k] else ""
        nx2 = norm(mots[i+k+1]) if i+k+1 < N and not debut[i+k+1] else ""

        # Score ARTICLE (facteur de rejet)
        if pv in ARTICLES:
            art += 1

        # ============================================================
        # PRIORITE : evidence PERSONNE verifiee EN PREMIER
        # Evite que "dit a Baley" soit classe lieu a cause de "a"
        # ============================================================
        if pv in TITRES:
            pers += 1

        elif pv in tous_verbes_pers:
            # Verbe de parole/action directement avant : "dit Baley"
            pers += 1

        elif nx in tous_verbes_pers or nx2 in tous_verbes_pers:
            # Verbe de parole/action directement apres : "Baley dit"
            pers += 1

        elif nx in verbes:
            # Verbe general apres (verbs.json)
            pers += 1

        # ============================================================
        # Evidence LIEU : seulement si pas deja compte comme personne
        # ============================================================
        elif pv in PREP:
            # Preposition forte directement avant : "dans Spacetown",
            # "par Spacetown", "en Trantor", "vers New York"
            lieu += 1

        elif pv in _DE_PREPS and (p2 in NLIEU or p3 in NLIEU):
            # "de/du/des/d'" + Nom MAIS seulement si precede d'un mot
            # de lieu : "rues de New York", "Police de New York"
            # Evite faux positif : "la femme de Baley" (femme pas dans NLIEU)
            lieu += 1

        elif p2 in NLIEU or p3 in NLIEU:
            # Mot de lieu 2 ou 3 positions avant : "la ville Trantor",
            # "la planete Kalgash"
            lieu += 1

        elif pv in tous_verbes_lieu or nx in tous_verbes_lieu:
            # Verbe de deplacement avant ou apres
            lieu += 1

    return milieu, pers, lieu, art
