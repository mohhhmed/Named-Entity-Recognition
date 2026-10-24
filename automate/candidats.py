from config import MOT, ROMAIN, TITRES, FICHIERS
from normalisation import norm

def extraire_candidats(interdits, propres):
    def valide(t):
        n = norm(t)
        return t[0].isupper() and len(t) >= 2 and not ROMAIN.match(t) \
               and (n in TITRES or n in propres or n not in interdits)

    cands = set()
    for fic in FICHIERS:
        try:
            for ligne in open(fic, encoding="utf-8"):
                suite = []
                for t in MOT.findall(ligne):
                    if valide(t):
                        suite.append(t)
                    elif suite:
                        while suite and norm(suite[0]) in TITRES: suite = suite[1:]
                        if suite: cands.add(tuple(suite))
                        suite = []
                while suite and norm(suite[0]) in TITRES: suite = suite[1:]
                if suite: cands.add(tuple(suite))
        except FileNotFoundError:
            print("ATTENTION:", fic, "manquant")
    return cands
