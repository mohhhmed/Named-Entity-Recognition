"""
Step 1 - Decoupage en phrases
- Couper aux signes . ! ? ... (mais pas apres les abreviations)
- Proteger les noms de robots : R. Daneel, R. Sammy...
- Une phrase par ligne dans le fichier de sortie
"""

import re

# Marqueur temporaire pour proteger les points d'abreviation
_PLACEHOLDER = "\x00"

# Abreviations qui ne terminent PAS une phrase
# AJOUT : R (robots d'Asimov : R. Daneel, R. Sammy, R. Giskard...)
_ABBREVS = re.compile(
    r"\b("
    r"M|Mme|Mlle|Dr|Pr|Prof|St|Ste|Sgt|Cdt|Lt|Cpt|Col|Gen|Gov|Pres"
    r"|vol|p|art|cf|ex|fig|ibid|id|loc|op|sq|vs|etc|env|apr|av|blvd"
    r"|R"        # <-- AJOUT : prefixe robot (R. Daneel Olivaw)
    r")\."
    r"(?=\s+[A-ZÀ-ÖØ-Ý0-9])",
    re.UNICODE,
)

# Dialogue : "- Texte", "– Texte" -> pas une frontiere de phrase
_DIALOGUE = re.compile(r"\n\s*[-–]\s+")


def split_sentences(input_path: str, output_path: str) -> None:
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Proteger les abreviations
    text = _ABBREVS.sub(lambda m: m.group(0).replace(".", _PLACEHOLDER), text)

    # Proteger les ellipses "..." qui ne terminent pas une phrase
    # (remplacer par placeholder si suivis d'une minuscule)
    text = re.sub(r"\.\.\.", _PLACEHOLDER * 3, text)

    # Decouper aux vraies fins de phrase
    sentences = re.split(r"(?<=[.!?])\s+", text)

    with open(output_path, "w", encoding="utf-8") as f:
        for sent in sentences:
            sent = sent.replace(_PLACEHOLDER, ".").strip()
            if sent:
                f.write(sent + "\n")

    print(f"[step1] Phrases -> {output_path}")
