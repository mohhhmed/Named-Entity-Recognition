"""
Step 0 - Preparation du corpus
- Lecture avec detection automatique d'encodage
- Reparation des cesures (mots coupes en fin de ligne)
- Normalisation des espaces, guillemets et apostrophes
- Correction des sequences double-encodees (UTF-8 lu comme cp1252)
- Garder les majuscules et la ponctuation
"""

import re


# Sequences typiques d'UTF-8 lu comme cp1252 puis re-encode UTF-8
# Ces remplacements corrigent la double-encodage la plus frequente
_DOUBLE_ENCODE_FIXES = [
    # Apostrophe UTF-8 (U+2019) lue comme cp1252 -> a euro trademark
    ("â€™",  "'"),
    ("â\u20ac\u2122", "'"),
    # e accent aigu (U+00E9)
    ("Ã©",   "é"),
    ("Ã\xa9", "é"),
    # e accent grave (U+00E8)
    ("Ã¨",   "è"),
    # e accent circonflexe (U+00EA)
    ("Ãª",   "ê"),
    # a accent grave (U+00E0)
    ("Ã ",   "à"),
    # u accent grave (U+00F9)
    ("Ã¹",   "ù"),
    # u accent circonflexe (U+00FB)
    ("Ã»",   "û"),
    # i accent circonflexe (U+00EE)
    ("Ã®",   "î"),
    # o accent circonflexe (U+00F4)
    ("Ã´",   "ô"),
    # c cedille (U+00E7)
    ("Ã§",   "ç"),
    # Guillemets typographiques
    ("â€œ",  "\u201c"),
    ("â€\x9d", "\u201d"),
    # Tirets longs
    ("\u00e2\u20ac\u201c",  "\u2014"),   # em-dash
    ("\u00e2\u20ac\u201d",  "\u2013"),   # en-dash
    # Espace insecable
    ("Â ",   " "),
    ("Â\xa0", " "),
    # Guillemets francais
    ("Â«",   "«"),
    ("Â»",   "»"),
    # Capital E accent aigu (U+00C9)
    ("Ã\x89", "É"),
    ("Ã‰",   "É"),
]


def _detect_and_read(path: str) -> str:
    """
    Essaie plusieurs encodages dans l'ordre et retourne le texte propre.
    UTF-8 et ses variantes d'abord (les fichiers Kaggle sont UTF-8).
    """
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, LookupError):
            continue
    # latin-1 ne leve jamais d'exception — securite
    with open(path, "rb") as f:
        return f.read().decode("latin-1", errors="replace")


def prepare(input_path: str, output_path: str) -> None:
    text = _detect_and_read(input_path)

    # Corriger les sequences double-encodees eventuelles
    for bad, good in _DOUBLE_ENCODE_FIXES:
        text = text.replace(bad, good)

    # Normaliser CRLF -> LF
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Reparer les cesures : mot-\n suite -> motsuite si minuscule suit
    text = re.sub(r"-\n([a-zàâäéèêëîïôùûüç])", r"\1", text)

    # Normaliser les guillemets typographiques -> guillemets droits
    text = text.replace("«", '"').replace("»", '"')
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2039", "'").replace("\u203a", "'")

    # Normaliser les apostrophes typographiques -> apostrophe droite
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u02bc", "'")

    # Normaliser les tirets longs
    text = text.replace("\u2014", " - ").replace("\u2013", " - ")

    # Supprimer les caracteres de controle (sauf \n et \t)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

    # Normaliser les espaces multiples et tabulations
    text = re.sub(r"[ \t]+", " ", text)

    # Convertir les mots TOUT-EN-MAJUSCULES (3+ chars) en Titre-Casse
    # Seuil 3 (pas 4) pour capturer "NEW" -> "New", "NEW YORK" -> "New York"
    text = re.sub(r"\b([A-Z]{3,})\b", lambda m: m.group(0).title(), text)

    # Supprimer espaces en debut/fin de ligne + lignes vides consecutives
    lines   = [l.strip() for l in text.split("\n")]
    cleaned = []
    prev_empty = False
    for line in lines:
        if line == "":
            if not prev_empty:
                cleaned.append(line)
            prev_empty = True
        else:
            cleaned.append(line)
            prev_empty = False

    text = "\n".join(cleaned)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"[step0] Corpus prepare -> {output_path}")
