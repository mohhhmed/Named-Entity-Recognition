from collections import defaultdict

def regrouper_alias(personnages):
    noms = sorted(personnages, key=len, reverse=True)
    alias, canon = defaultdict(list), {}
    for n in noms:
        parent = next((f for f in canon.values() if len(f) > len(n) and all(t in f for t in n)), None)
        if parent: alias[" ".join(parent)].append(" ".join(n)); canon[n] = parent
        else: canon[n] = n
    return noms, alias, canon
