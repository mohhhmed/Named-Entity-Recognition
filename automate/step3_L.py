"""
Step 3 - Construction de L (Tache 1)
- Garder les n-grammes (1, 2, 3, 4) dont le premier token commence par une majuscule
- Ecrire candidat<TAB>frequence en UTF-8, sans filtrage

CORRECTION : regex French uppercase chars (A-Z + accented A-Z : A-ZA-OO-Y was BROKEN)
"""

import re
from collections import Counter

# Regex correcte pour les majuscules francaises
# [A-ZA-OO-Y] etait faux — correct : [A-ZA-OO-Y] couvre
# A-Z (ASCII) + A-O (U+00C0..U+00D6) + O-Y (U+00D8..U+00DD)
# en notation Python : \u00C0-\u00D6\u00D8-\u00DD
_UPPER_FR = re.compile(
    r"\b[A-Z\u00C0-\u00D6\u00D8-\u00DD][\w\u00C0-\u00FF'-]*\b",
    re.UNICODE,
)


def build_L(
    corpus_path: str,
    n2_path: str,
    n3_path: str,
    n4_path: str,
    output_path: str,
) -> None:
    compteur: Counter = Counter()

    # 1-grammes : tous les tokens majuscules du corpus (regex corrigee)
    with open(corpus_path, "r", encoding="utf-8") as f:
        texte = f.read()

    for mot in _UPPER_FR.findall(texte):
        compteur[mot] += 1

    # 2-grammes
    with open(n2_path, "r", encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if ligne:
                compteur[ligne] += 1

    # 3-grammes
    with open(n3_path, "r", encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if ligne:
                compteur[ligne] += 1

    # 4-grammes
    with open(n4_path, "r", encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if ligne:
                compteur[ligne] += 1

    # Ecrire candidat<TAB>frequence, trie par frequence decroissante
    with open(output_path, "w", encoding="utf-8") as f:
        for candidat, freq in sorted(compteur.items(), key=lambda x: -x[1]):
            f.write(f"{candidat}\t{freq}\n")

    print(f"[step3] Liste L -> {output_path}  ({len(compteur)} entrees)")
