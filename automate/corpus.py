from collections import Counter, defaultdict
import config
from config import MOT, FIN, TITRES
from normalisation import norm

def indexer_corpus():
    texte = open(config.CORPUS_FILE, encoding="utf-8").read()
    mots, debut, fin = [], [], 0
    for m in MOT.finditer(texte):
        gap = texte[fin:m.start()]
        d = not mots or bool(FIN.search(gap))
        if mots and norm(mots[-1]) in TITRES and gap.strip() == ".": d = False
        mots.append(m.group()); debut.append(d); fin = m.end()

    pos = defaultdict(list)
    for i, w in enumerate(mots): pos[w].append(i)

    minus = Counter(norm(w) for w in mots if w[0].islower())
    maj   = Counter(norm(w) for w, d in zip(mots, debut) if w[0].isupper() and not d)
    propres = {n for n in maj if maj[n] >= 2 and minus[n] <= 0.1 * maj[n]}
    return mots, debut, pos, propres
